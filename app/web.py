
import os
import time

import psycopg2
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "bitsec_db"),
        user=os.getenv("POSTGRES_USER", "bitsec_user"),
        password=os.getenv("POSTGRES_PASSWORD", "")
    )


def initialize_database():
    for attempt in range(10):
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS calculations (
                            id SERIAL PRIMARY KEY,
                            operation VARCHAR(20) NOT NULL,
                            number_a DOUBLE PRECISION NOT NULL,
                            number_b DOUBLE PRECISION NOT NULL,
                            result DOUBLE PRECISION NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
            print("Database initialized successfully.")
            return
        except psycopg2.OperationalError:
            print(f"Database unavailable. Attempt {attempt + 1}/10")
            time.sleep(3)

    raise RuntimeError("Could not connect to PostgreSQL.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except psycopg2.Error:
        return jsonify({
            "status": "unhealthy",
            "database": "unavailable"
        }), 503


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}

    operation = data.get("operation")
    a = data.get("a")
    b = data.get("b")

    if operation not in ["add", "subtract", "multiply", "divide"]:
        return jsonify({"error": "Invalid operation"}), 400

    try:
        a = float(a)
        b = float(b)

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        else:
            if b == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = a / b

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO calculations
                    (operation, number_a, number_b, result)
                    VALUES (%s, %s, %s, %s)
                """, (operation, a, b, result))

        return jsonify({
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        }), 200

    except (TypeError, ValueError):
        return jsonify({"error": "Please provide valid numbers"}), 400

    except psycopg2.Error:
        return jsonify({"error": "Database operation failed"}), 503


@app.route("/history")
def history():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, operation, number_a, number_b,
                           result, created_at
                    FROM calculations
                    ORDER BY id DESC
                    LIMIT 50
                """)

                rows = cursor.fetchall()

        return jsonify([
            {
                "id": row[0],
                "operation": row[1],
                "a": row[2],
                "b": row[3],
                "result": row[4],
                "created_at": row[5].isoformat()
            }
            for row in rows
        ])

    except psycopg2.Error:
        return jsonify({"error": "Could not retrieve calculation history"}), 503


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)

