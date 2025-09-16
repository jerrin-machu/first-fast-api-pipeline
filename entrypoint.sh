#!/usr/bin/env bash
set -euo pipefail


echo "Waiting for DB..."
python /app/wait_for_db.py


# If you use Alembic, run migrations here (optional)
if [ -f ./alembic.ini ]; then
echo "Running alembic migrations..."
alembic upgrade head
fi


# Start uvicorn (no --reload in prod)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000