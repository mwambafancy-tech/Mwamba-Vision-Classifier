#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${REPO_NAME:-Mwamba-Vision-Classifier}"
VISIBILITY="${VISIBILITY:-public}"

printf "GitHub username: "
read -r GITHUB_USER

printf "GitHub token (hidden): "
stty -echo
read -r GITHUB_TOKEN
stty echo
printf "\n"

if [ -z "$GITHUB_USER" ] || [ -z "$GITHUB_TOKEN" ]; then
  echo "Username and token are required."
  exit 1
fi

export GITHUB_USER
export GITHUB_TOKEN

if [ "$VISIBILITY" = "private" ]; then
  PRIVATE_VALUE=true
else
  PRIVATE_VALUE=false
fi

echo "Creating GitHub repository: ${GITHUB_USER}/${REPO_NAME}"
CREATE_RESPONSE="$(curl -sS -o /tmp/mwamba_github_create_repo.json -w "%{http_code}" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"${REPO_NAME}\",\"private\":${PRIVATE_VALUE},\"description\":\"Android TensorFlow Lite image classifier built by Mwamba Mutale.\"}")"

if [ "$CREATE_RESPONSE" != "201" ] && [ "$CREATE_RESPONSE" != "422" ]; then
  echo "GitHub repository creation failed. Response:"
  cat /tmp/mwamba_github_create_repo.json
  exit 1
fi

if [ "$CREATE_RESPONSE" = "422" ]; then
  echo "Repository may already exist. Continuing with push."
fi

git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

ASKPASS_FILE="$(mktemp /tmp/mwamba_git_askpass.XXXXXX)"
trap 'rm -f "$ASKPASS_FILE"' EXIT
cat > "$ASKPASS_FILE" <<'ASKPASS'
#!/usr/bin/env bash
case "$1" in
  *Username*) printf "%s" "$GITHUB_USER" ;;
  *Password*) printf "%s" "$GITHUB_TOKEN" ;;
  *) printf "" ;;
esac
ASKPASS
chmod 700 "$ASKPASS_FILE"

echo "Pushing code to GitHub..."
GIT_ASKPASS="$ASKPASS_FILE" GIT_TERMINAL_PROMPT=0 git -c credential.helper= push -u origin main

echo "Done: https://github.com/${GITHUB_USER}/${REPO_NAME}"
