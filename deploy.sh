#!/usr/bin/env bash
set -euo pipefail


APP_DIR="/srv/my-fastapi-app"
COMPOSE_FILE="${APP_DIR}/docker-compose.prod.yml"


if [ ! -f "${COMPOSE_FILE}" ]; then
echo "Compose file not found at ${COMPOSE_FILE}" >&2
exit 1
fi


if [ -z "${IMAGE:-}" ]; then
echo "Usage: IMAGE=yourrepo/fastapi-app:tag $0" >&2
exit 1
fi


TAG="${IMAGE##*:}"
cd "${APP_DIR}"


# Create .env if missing (safe defaults shown; replace as needed)
if [ ! -f .env ]; then
cat > .env <<EOF
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
POSTGRES_DB=${POSTGRES_DB:-postgres}
DB_HOST=db
DB_PORT=${DB_PORT:-5432}
EOF
echo ".env created"
fi


# Pull image and update just the web service
docker pull "${IMAGE}"
TAG="${TAG}" docker compose -f "${COMPOSE_FILE}" up -d --no-deps --no-build web


docker compose -f "${COMPOSE_FILE}" ps


echo "Deploy finished"