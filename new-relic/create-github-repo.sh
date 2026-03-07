#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash create-github-repo.sh <github-username>"
  exit 1
fi

GITHUB_USERNAME="$1"
REPO_NAME="new-relic"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI (gh) is not installed."
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Error: gh is not authenticated. Run: gh auth login"
  exit 1
fi

if [[ ! -d .git ]]; then
  git init
fi

git add .

if git diff --cached --quiet; then
  echo "No staged changes to commit. Continuing..."
else
  git commit -m "Initial commit for New Relic project"
fi

git branch -M main

gh repo create "${GITHUB_USERNAME}/${REPO_NAME}" --private --source=. --remote=origin --push

echo "Done: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
