#!/bin/bash

# Extract the TAG from kustomization.yaml using yq
export TAG=$(yq '.images[].newTag' k8s/overlays/prod/kustomization.yaml)

# Validate that TAG is set
if [ -z "$TAG" ]; then
    echo "Error: TAG is not set in kustomization.yaml. Please ensure it is defined."
    exit 1
fi

# Extract IMAGE_PREFIX from the Azure account
IMAGE_PREFIX=$(az account list --all | jq '.[].user.name' | grep -i berkeley.edu | awk -F@ '{print $1}' | tr -d '"' | tr -d "." | tr '[:upper:]' '[:lower:]' | tr '_' '-' | uniq)

# Set image details
IMAGE_NAME="project"
ACR_DOMAIN="w255mids.azurecr.io"
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}:${TAG}"

# Authenticate to ACR
echo "Logging into Azure Container Registry..."
az acr login --name w255mids

# Pull the image
echo "Pulling image: ${IMAGE_FQDN}"
docker pull "${IMAGE_FQDN}"

# Output confirmation
echo "Image pulled successfully: ${IMAGE_FQDN}"
echo "Tag used: $TAG"