#!/bin/bash
set -e

WEBHOOK_FILE="webhook-config.yaml"
SERVICE_NAME="k8s-yaml-analyzer"
NAMESPACE="default"

# Create CA key + cert
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -subj "/CN=Admission CA" -out ca.crt

# Patch caBundle
CA_BUNDLE=$(cat ca.crt | base64 | tr -d '\n')

sed -i.bak "s|caBundle:.*|caBundle: \"$CA_BUNDLE\"|g" $WEBHOOK_FILE

echo "Patched $WEBHOOK_FILE with new CA bundle."
