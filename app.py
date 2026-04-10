from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "/tmp/projects.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image TEXT,
            description TEXT,
            date TEXT,
            download TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/projects", methods=["GET"])
def projects():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "name": r[1],
            "image": r[2],
            "description": r[3],
            "date": r[4],
            "download": r[5]
        }
        for r in rows
    ])

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(silent=True) or {}

    required = ["name", "image", "description", "date", "download"]
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO projects(name,image,description,date,download)
        VALUES (?,?,?,?,?)
    """, (data["name"], data["image"], data["description"], data["date"], data["download"]))
    conn.commit()
    conn.close()

    return jsonify({"ok": True})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
