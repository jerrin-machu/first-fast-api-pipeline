import os
from tenacity import retry, wait_fixed, stop_after_delay
import psycopg2
import sys


@retry(wait=wait_fixed(2), stop=stop_after_delay(60))
def wait_for_db():
    host = os.getenv("DB_HOST", "db")
    port = int(os.getenv("DB_PORT", 5432))
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    dbname = os.getenv("POSTGRES_DB", "postgres")

    print(f"Trying to connect to Postgres at {host}:{port} as {user}...")
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )
    conn.close()
    print("Connected to Postgres ✅")


if __name__ == '__main__':
    try:
        wait_for_db()
        sys.exit(0)   # exit cleanly after success
    except Exception as e:
        print("❌ Timed out waiting for Postgres:", e)
        sys.exit(1)
