#!/bin/bash
set -euo pipefail
set -x

if [ $# -ne 3 ]; then
  echo "Usage: $0 <service> <image-repo> <tag>"
  exit 1
fi

SERVICE="$1"
IMAGE_REPO="$2"
TAG="$3"

# Expect AZURE_PAT and AZURE_REPO_HTTPS to be set, e.g.:
# AZURE_REPO_HTTPS=https://dev.azure.com/<org>/<project>/_git/<repo>
: "${AZURE_PAT?Need AZURE_PAT env var}"
: "${AZURE_REPO_HTTPS?Need AZURE_REPO_HTTPS env var}"

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

# Insert PAT into URL safely
AUTH_URL="${AZURE_REPO_HTTPS/https:\/\//https://${AZURE_PAT}@}"

git clone "$AUTH_URL" "$WORKDIR/repo"
cd "$WORKDIR/repo"

FILE="k8s-specifications/${SERVICE}-deployment.yaml"
if [ ! -f "$FILE" ]; then
  echo "Manifest $FILE not found"
  exit 1
fi

# Replace image line
# Example target: image: gabvotingappacr.azurecr.io/votingapp/vote:18
sed -i "s|^\([[:space:]]*image:\s*\).*|\1${IMAGE_REPO}/${SERVICE}:${TAG}|" "$FILE"

git config user.email "ci@local"
git config user.name "CI Bot"

git add "$FILE"
if git diff --cached --quiet; then
  echo "No changes detected"
  exit 0
fi

git commit -m "chore(${SERVICE}): update image to ${IMAGE_REPO}/${SERVICE}:${TAG}"
git push origin HEAD
