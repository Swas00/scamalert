#!/usr/bin/env bash
# Runs the whole ScamAlert API in ONE container/process group: the Python classifier (loopback only) and the Node backend (public).
# Either process dying stops the other and exits non-zero, so the hosting platform restarts the service instead of leaving half of it up.
#
# Environment: PORT (public port; default 7860), APP_DIR (default /app), PYTHON (default python3), CLASSIFIER_PORT (default 8000).
# Secrets the backend/classifier read: GNANI_API_KEY, MONGODB_URI (optional), FRONTEND_ORIGIN, RATE_LIMIT_PER_HOUR, INTERNAL_TOKEN (optional).
# Written for plain POSIX-style bash (no `wait -n`, no arrays) so it behaves the same on old and new shells.
set -eu

APP_DIR="${APP_DIR:-/app}"
PYTHON="${PYTHON:-python3}"
CLASSIFIER_PORT="${CLASSIFIER_PORT:-8000}"
export PORT="${PORT:-7860}"
# The classifier listens on 127.0.0.1 only, so nothing outside the container can reach it; the backend talks to it locally.
export CLASSIFIER_URL="http://127.0.0.1:${CLASSIFIER_PORT}"

CPID=""
BPID=""
cleanup() {
  [ -n "$BPID" ] && kill "$BPID" 2>/dev/null || true
  [ -n "$CPID" ] && kill "$CPID" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 143' TERM INT

echo "[start] classifier on 127.0.0.1:${CLASSIFIER_PORT}"
( cd "$APP_DIR/classifier" && exec "$PYTHON" -m uvicorn main:app --host 127.0.0.1 --port "$CLASSIFIER_PORT" ) &
CPID=$!

# Wait (up to 60 s) for the classifier before opening the public port, so the first request never hits a half-started service.
i=0
while :; do
  i=$((i + 1))
  if curl -fsS "http://127.0.0.1:${CLASSIFIER_PORT}/health" >/dev/null 2>&1; then echo "[start] classifier ready after ${i}s"; break; fi
  if ! kill -0 "$CPID" 2>/dev/null; then echo "[start] classifier exited during start-up" >&2; exit 1; fi
  if [ "$i" -ge 60 ]; then echo "[start] classifier did not become healthy in 60s" >&2; exit 1; fi
  sleep 1
done

echo "[start] backend on 0.0.0.0:${PORT}"
( cd "$APP_DIR/backend" && exec node server.js ) &
BPID=$!

# Watch both processes; if either is gone, stop the container so the platform restarts it.
while kill -0 "$CPID" 2>/dev/null && kill -0 "$BPID" 2>/dev/null; do
  sleep 1
done
if kill -0 "$CPID" 2>/dev/null; then echo "[start] the backend exited; stopping the container" >&2
else echo "[start] the classifier exited; stopping the container" >&2; fi
exit 1
