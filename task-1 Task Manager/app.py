from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "tasks.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Task Management API is running",
        "endpoints": {
            "GET": "/tasks",
            "GET": "/tasks/<id>",
            "POST": "/tasks",
            "PUT": "/tasks/<id>",
            "DELETE": "/tasks/<id>"
        }
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    return jsonify([dict(task) for task in tasks]), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(task)), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title is required and must be a non-empty string"
        }), 400

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be a string"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, completed)
        VALUES (?, ?, ?)
        """,
        (title.strip(), description.strip(), 0)
    )

    connection.commit()

    task_id = cursor.lastrowid

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(task)), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")

    if title is None or description is None or completed is None:
        return jsonify({
            "error": "title, description and completed are required"
        }), 400

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title must be a non-empty string"
        }), 400

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be a string"
        }), 400

    if not isinstance(completed, bool):
        return jsonify({
            "error": "Completed must be true or false"
        }), 400

    connection = get_db_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        return jsonify({"error": "Task not found"}), 404

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (
            title.strip(),
            description.strip(),
            int(completed),
            task_id
        )
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(updated_task)), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = get_db_connection()

    existing_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing_task is None:
        connection.close()
        return jsonify({"error": "Task not found"}), 404

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "HTTP method not allowed for this endpoint"
    }), 405


if __name__ == "__main__":
    initialize_database()

    print("=" * 60)
    print("             TASK MANAGEMENT API")
    print("=" * 60)
    print("Server running at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")

    app.run(debug=True)