# One image for the whole ScamAlert API: Node backend (public) + Python classifier (loopback only), started by deploy/start.sh.
# Runs on Render (Docker runtime), Hugging Face Spaces (Docker SDK, port 7860), Fly, Koyeb or anywhere that runs a container.
FROM node:22-bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv python3-pip curl ca-certificates bash \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies first (cached unless requirements change). A venv avoids Debian's "externally managed" pip restriction.
# requirements.lock pins the exact versions the tests passed with, so a rebuild can never pull newer, untested releases.
COPY classifier/requirements.lock classifier/requirements.lock
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --no-deps -r classifier/requirements.lock

# Node dependencies (production only), from the lockfile.
COPY backend/package.json backend/package-lock.json backend/
RUN cd backend && npm ci --omit=dev

# Application code (node_modules / venv / tests are excluded by .dockerignore).
COPY classifier classifier
COPY backend backend
COPY deploy/start.sh /app/start.sh

# Hugging Face Spaces expects port 7860 and a non-root user with uid 1000 (the built-in "node" user). Render overrides PORT.
ENV PYTHON=/opt/venv/bin/python PORT=7860 NODE_ENV=production
RUN chown -R node:node /app
USER node
EXPOSE 7860

CMD ["bash", "/app/start.sh"]
