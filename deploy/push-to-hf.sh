#!/usr/bin/env bash
# Publish the API container to a Hugging Face Space (Docker SDK) in one step.
#
# 1. Create a Space at https://huggingface.co/new-space  (SDK: Docker, template: Blank, visibility: Public or Private).
# 2. Settings -> "Variables and secrets": add GNANI_API_KEY and FRONTEND_ORIGIN (and MONGODB_URI if you want usage stats).
# 3. Run:   deploy/push-to-hf.sh https://huggingface.co/spaces/<user>/<space>
#    Git asks for your username and a WRITE access token as the password (https://huggingface.co/settings/tokens).
set -euo pipefail

SPACE_URL="${1:?usage: deploy/push-to-hf.sh https://huggingface.co/spaces/<user>/<space>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

git clone "$SPACE_URL" "$WORK/space"
cd "$WORK/space"

# Replace the Space's contents with exactly what the image needs (never any .env, node_modules or virtualenv).
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
mkdir -p classifier backend deploy
rsync -a --exclude node_modules --exclude venv --exclude __pycache__ --exclude '*.pyc' --exclude .env --exclude .pytest_cache --exclude tests --exclude requirements-dev.txt "$ROOT/classifier/" classifier/
rsync -a --exclude node_modules --exclude .env "$ROOT/backend/" backend/
cp "$ROOT/deploy/start.sh" deploy/start.sh
cp "$ROOT/Dockerfile" "$ROOT/.dockerignore" .
cp "$ROOT/deploy/hf-space-README.md" README.md

git add -A
if git diff --cached --quiet; then echo "Nothing to publish: the Space already matches this repository."; exit 0; fi
SRC_SHA="$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
git -c user.name="${GIT_AUTHOR_NAME:-$(git -C "$ROOT" config user.name || echo scamalert)}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-$(git -C "$ROOT" config user.email || echo scamalert@users.noreply.huggingface.co)}" \
    commit -q -m "Deploy ScamAlert API from GitHub ${SRC_SHA}"
git push origin HEAD:main
echo
echo "Pushed. The Space now builds the image (a few minutes). When it shows 'Running', check:"
echo "  https://<user>-<space>.hf.space/api/health"
echo "Then set VITE_API_URL to that address in Vercel and redeploy the frontend."
