"""
AttendTrack — Flask + SQLite Backend
=====================================
Serves the frontend at / and provides a REST API for attendance data.

Run:  python app.py
Then open:  http://localhost:5000
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory

# ─── App setup ────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

app = Flask(__name__, static_folder=BASE_DIR)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False


# ─── Database ─────────────────────────────────────────────────────────────────

def get_db():
    """Return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS rolls (
                roll_number TEXT PRIMARY KEY,
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS records (
                roll_number TEXT NOT NULL,
                data        TEXT NOT NULL,
                updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (roll_number)
            );

            CREATE TABLE IF NOT EXISTS subjects (
                roll_number TEXT NOT NULL,
                data        TEXT NOT NULL,
                updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
                PRIMARY KEY (roll_number)
            );
        """)
    print(f"[DB] Initialized at {DB_PATH}")


# ─── CORS helper ──────────────────────────────────────────────────────────────

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return jsonify({}), 200


# ─── Static files / Frontend ──────────────────────────────────────────────────

@app.route("/")
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    if filename.startswith(".") or filename.endswith(".db") or filename.endswith(".py") or filename == "requirements.txt":
        return jsonify({"error": "Access denied"}), 403
    return send_from_directory(BASE_DIR, filename)


# ─── API: Roll numbers ────────────────────────────────────────────────────────

@app.route("/api/rolls", methods=["GET"])
def get_rolls():
    """Return list of all known roll numbers."""
    with get_db() as conn:
        rows = conn.execute("SELECT roll_number FROM rolls ORDER BY created_at").fetchall()
    rolls = [r["roll_number"] for r in rows]
    return jsonify(rolls)


@app.route("/api/rolls", methods=["POST"])
def add_roll():
    """Register a roll number (idempotent)."""
    data = request.get_json(force=True)
    roll = (data.get("roll_number") or "").strip().upper()
    if not roll:
        return jsonify({"error": "roll_number is required"}), 400
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO rolls (roll_number) VALUES (?)", (roll,)
        )
    return jsonify({"ok": True, "roll_number": roll})


# ─── API: Attendance records ───────────────────────────────────────────────────

@app.route("/api/records/<roll>", methods=["GET"])
def get_records(roll):
    """Return all daily attendance records for a roll number."""
    roll = roll.strip().upper()
    with get_db() as conn:
        row = conn.execute(
            "SELECT data FROM records WHERE roll_number = ?", (roll,)
        ).fetchone()
    if row:
        return jsonify(json.loads(row["data"]))
    return jsonify({})


@app.route("/api/records/<roll>", methods=["POST"])
def save_records(roll):
    """Save (overwrite) all daily attendance records for a roll number."""
    roll = roll.strip().upper()
    payload = request.get_json(force=True)
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO records (roll_number, data, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(roll_number) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at""",
            (roll, json.dumps(payload), now),
        )
        conn.execute("INSERT OR IGNORE INTO rolls (roll_number) VALUES (?)", (roll,))
    return jsonify({"ok": True})


# ─── API: Subjects ─────────────────────────────────────────────────────────────

@app.route("/api/subjects/<roll>", methods=["GET"])
def get_subjects(roll):
    """Return subject list for a roll number."""
    roll = roll.strip().upper()
    with get_db() as conn:
        row = conn.execute(
            "SELECT data FROM subjects WHERE roll_number = ?", (roll,)
        ).fetchone()
    if row:
        return jsonify(json.loads(row["data"]))
    return jsonify(None)   # null → frontend will use defaults


@app.route("/api/subjects/<roll>", methods=["POST"])
def save_subjects(roll):
    """Save subject list for a roll number."""
    roll = roll.strip().upper()
    payload = request.get_json(force=True)
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO subjects (roll_number, data, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(roll_number) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at""",
            (roll, json.dumps(payload), now),
        )
        conn.execute("INSERT OR IGNORE INTO rolls (roll_number) VALUES (?)", (roll,))
    return jsonify({"ok": True})


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("=" * 55)
    print("  AttendTrack Backend")
    print("  Open: http://localhost:5000")
    print("  API:  http://localhost:5000/api/")
    print("  LAN:  http://<your-ip>:5000  (WiFi sharing)")
    print("=" * 55)
    app.run(debug=True, host="0.0.0.0", port=5000)
