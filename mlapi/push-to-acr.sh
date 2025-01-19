#!/bin/bash

# Generate a short git commit hash
export TAG=$(git rev-parse --short HEAD)

# Set the ACR registry, namespace, and image details
ACR_REGISTRY="w255mids.azurecr.io"
export NAMESPACE=$(az account list --all | jq '.[].user.name' | grep -i berkeley.edu | awk -F@ '{print $1}' | tr -d '"' | tr -d "." | tr '[:upper:]' '[:lower:]' | tr '_' '-' | uniq)
IMAGE_NAME="project"


# Build the Docker image
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .

# Tag the image for ACR
docker tag "${IMAGE_NAME}:${TAG}" "${ACR_REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${TAG}"

# Push the image to ACR
docker push "${ACR_REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${TAG}"

# Update kustomization.yaml with the new image tag
yq -i '.images[].newTag = env(TAG)' k8s/overlays/prod/kustomization.yaml

# NAMESPACE confirmation
echo "NAMESPACE: $NAMESPACE"
# Output confirmation
echo "Pushed image and updated kustomization.yaml with tag: $TAG"