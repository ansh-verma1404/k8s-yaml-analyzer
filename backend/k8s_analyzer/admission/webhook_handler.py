from typing import Dict, Any
import base64
import logging

logger = logging.getLogger("webhook_handler")

def _extract_uid(ar: Dict[str, Any]) -> str:
    try:
        return ar.get("request", {}).get("uid")
    except Exception:
        return None

def _get_object(ar: Dict[str, Any]):
    return ar.get("request", {}).get("object", {})


# --------------------------------------------------------------------------
# BYPASS RULES (IMPORTANT)
# --------------------------------------------------------------------------

def should_skip_validation(obj: Dict[str, Any]) -> bool:
    metadata = obj.get("metadata", {})
    name = metadata.get("name", "")
    labels = metadata.get("labels", {}) or {}
    namespace = metadata.get("namespace", "default")

    # Skip own analyzer components
    analyzer_names = ["analyzer-backend", "analyzer-frontend", "analyzer-webhook"]
    if any(n in name for n in analyzer_names):
        return True

    # Skip if special label exists
    if labels.get("skip-webhook") == "true":
        return True

    # Skip system namespaces
    if namespace in ["kube-system", "kube-public", "kube-node-lease"]:
        return True

    # Skip typical system pods (optional)
    if labels.get("app.kubernetes.io/name") in ["coredns", "kube-proxy"]:
        return True

    return False


def _find_container_images(obj: Dict[str, Any]):
    images = []
    # Pod spec
    try:
        pod_spec = obj.get("spec")
        if pod_spec:
            for c in pod_spec.get("containers", []):
                if c.get("image"):
                    images.append(c.get("image"))
    except Exception:
        pass

    # Deployment spec
    try:
        template_spec = obj.get("spec", {}).get("template", {}).get("spec", {})
        for c in template_spec.get("containers", []):
            if c.get("image"):
                images.append(c.get("image"))
    except Exception:
        pass

    return images


def _image_uses_latest_or_no_tag(image: str) -> bool:
    # Bypass analyzer images
    if image.startswith("ghcr.io/ansh-verma1404/k8s-yaml-analyzer-backend"):
        return False

    if "@" in image:
        image = image.split("@")[0]

    last_slash = image.rfind("/")
    remainder = image[last_slash + 1:]

    if ":" not in remainder:
        return True
    tag = remainder.split(":", 1)[1]
    return tag == "" or tag == "latest"


def admission_review_response(admission_review: Dict[str, Any]) -> Dict[str, Any]:
    uid = _extract_uid(admission_review)
    obj = _get_object(admission_review)
    images = _find_container_images(obj)

    # Skip validation for system/analyzer pods
    if should_skip_validation(obj):
        return {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": True,
                "status": {"message": "Validation skipped for internal/system components"}
            }
        }, 200

    allowed = True
    messages = []

    # Normal rule: deny images without tag or with latest
    for image in images:
        if _image_uses_latest_or_no_tag(image):
            allowed = False
            messages.append(f"Disallowed image tag in {image} (no tag or :latest).")

    if not images:
        messages.append("No containers detected; allowed.")

    status = {"message": "; ".join(messages)} if messages else None

    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": allowed
        }
    }
    if status:
        response["response"]["status"] = status

    return response, 200
