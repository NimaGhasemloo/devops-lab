from flask import Flask, jsonify
import os
import psycopg

app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


@app.route("/")
def home():
    return "DevOps API is running!"


@app.route("/users")
def users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users ORDER BY id")
            rows = cur.fetchall()

    return jsonify([
        {"id": row[0], "name": row[1]}
        for row in rows
    ])

@app.route("/health")
@app.route("/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return {"status": "healthy"}, 200

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503
app.run(host="0.0.0.0", port=8000)
