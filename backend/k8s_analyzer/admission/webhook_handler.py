# backend/app/admission/webhook_handler.py
"""
Simple admission handler.
- Expects an AdmissionReview v1 request (dict).
- Returns a dict representing an AdmissionReview v1 response.

This implementation contains an example rule:
- Deny Pod/Deployment creations that use container images with tag 'latest' or no tag.
- Allow everything else.

You should expand this by calling your analyzer.* modules (schema_validator, security_checks, best_practices)
and including richer messages / patches as needed.
"""

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
    # AdmissionReview v1: payload under request.object
    return ar.get("request", {}).get("object", {})

def _find_container_images(obj: Dict[str, Any]):
    """
    Walk the object to find container image strings (works for Pod specs and Deployment specs).
    Returns list of image strings.
    """
    images = []
    # Pod spec path: spec.containers
    try:
        # For Pod
        pod_spec = obj.get("spec")
        if pod_spec:
            containers = pod_spec.get("containers", [])
            for c in containers:
                maybe_image = c.get("image")
                if maybe_image:
                    images.append(maybe_image)
    except Exception:
        pass

    # For Deployment/ReplicaSet, containers live at spec.template.spec.containers
    try:
        template_spec = obj.get("spec", {}).get("template", {}).get("spec", {})
        containers = template_spec.get("containers", [])
        for c in containers:
            maybe_image = c.get("image")
            if maybe_image:
                images.append(maybe_image)
    except Exception:
        pass

    return images

def _image_uses_latest_or_no_tag(image: str) -> bool:
    """
    Return True if image uses :latest or has no explicit tag (e.g. 'nginx' or 'nginx:latest').
    We treat image strings with no ':' after last '/' as no tag.
    """
    # Split off digest if present
    if "@" in image:
        image = image.split("@")[0]
    # If there's a colon after the last slash, that's a tag.
    last_slash = image.rfind("/")
    remainder = image[last_slash+1:]
    if ":" not in remainder:
        # no tag -> treat as latest-like (deny)
        return True
    tag = remainder.split(":", 1)[1]
    if tag == "" or tag == "latest":
        return True
    return False

def admission_review_response(admission_review: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return an AdmissionReview dict compatible with admission.k8s.io/v1.
    The returned object MUST be:
    {
      "apiVersion": "admission.k8s.io/v1",
      "kind": "AdmissionReview",
      "response": {
         "uid": "<incoming-uid>",
         "allowed": true|false,
         "status": { "message": "..." }  # optional
      }
    }
    """
    uid = _extract_uid(admission_review)
    obj = _get_object(admission_review)
    images = _find_container_images(obj)

    # Default allow
    allowed = True
    messages = []

    # Example validation: deny images with :latest or no tag
    for image in images:
        if _image_uses_latest_or_no_tag(image):
            allowed = False
            messages.append(f"Disallowed image tag in {image} (no tag or :latest).")

    # Example: if no containers detected, allow (or you can choose otherwise)
    if not images:
        # Not a workload with containers (or structure unexpected) — allow but warn
        messages.append("No container images detected in object; allowed by default.")

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

    return response
