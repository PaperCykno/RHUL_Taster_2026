import re
import sqlite3
import time
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ghost_team.db"

UNLOCK_CODE = "73-47-91-4F2Q"
FLAG = "rhul{ghosts_leave_audit_trails}"

MAX_ROWS = 200
MAX_QUERY_LENGTH = 5000

SAFE_PRAGMAS = {
  "table_info",
  "table_xinfo",
  "index_list",
  "index_info",
  "foreign_key_list"
}


def authorizer(
  action,
  arg1,
  arg2,
  database_name,
  trigger_name
):
  denied_actions = {
    getattr(sqlite3, "SQLITE_INSERT", -100),
    getattr(sqlite3, "SQLITE_UPDATE", -101),
    getattr(sqlite3, "SQLITE_DELETE", -102),
    getattr(sqlite3, "SQLITE_CREATE_TABLE", -103),
    getattr(sqlite3, "SQLITE_DROP_TABLE", -104),
    getattr(sqlite3, "SQLITE_ALTER_TABLE", -105),
    getattr(sqlite3, "SQLITE_CREATE_INDEX", -106),
    getattr(sqlite3, "SQLITE_DROP_INDEX", -107),
    getattr(sqlite3, "SQLITE_CREATE_TRIGGER", -108),
    getattr(sqlite3, "SQLITE_DROP_TRIGGER", -109),
    getattr(sqlite3, "SQLITE_ATTACH", -110),
    getattr(sqlite3, "SQLITE_DETACH", -111),
    getattr(sqlite3, "SQLITE_TRANSACTION", -112),
    getattr(sqlite3, "SQLITE_SAVEPOINT", -113)
  }

  if action in denied_actions:
    return sqlite3.SQLITE_DENY

  if action == getattr(
    sqlite3,
    "SQLITE_PRAGMA",
    -114
  ):
    pragma_name = (
      arg1 or ""
    ).lower()

    if pragma_name not in SAFE_PRAGMAS:
      return sqlite3.SQLITE_DENY

  if action == getattr(
    sqlite3,
    "SQLITE_FUNCTION",
    -115
  ):
    function_name = (
      arg2 or arg1 or ""
    ).lower()

    if function_name in {
      "load_extension",
      "readfile",
      "writefile"
    }:
      return sqlite3.SQLITE_DENY
  return sqlite3.SQLITE_OK


def get_connection():
  connection = sqlite3.connect(
    DB_PATH,
    timeout=2
  )

  connection.execute("PRAGMA query_only = ON")
  connection.set_authorizer(authorizer)

  try:
    connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 1_000_000)
    connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH,10_000)
    connection.setlimit(sqlite3.SQLITE_LIMIT_COLUMN, 100)
    connection.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 50)
  except AttributeError:
    pass

  progress_steps = [0]

  def progress_handler():
    progress_steps[0] += 1

    if progress_steps[0] > 3000:
      return 1

    return 0

  connection.set_progress_handler(progress_handler, 1000)

  return connection


def validate_query(query):
  query = query.strip()

  if not query:
    return False, "Enter a SQL query."

  if len(query) > MAX_QUERY_LENGTH:
    return False, "Query is too long."


  if re.match(
    r"^SELECT\b",
    query,
    re.IGNORECASE
  ):
    return True, None

  if re.match(
    r"^WITH\b",
    query,
    re.IGNORECASE
  ):
    return True, None

  if re.match(
    r"^EXPLAIN\s+QUERY\s+PLAN\s+(SELECT|WITH)\b",
    query,
    re.IGNORECASE
  ):
    return True, None

  pragma_match = re.match(
    r"^PRAGMA\s+([A-Za-z0-9_]+)",
    query,
    re.IGNORECASE
  )

  if pragma_match:
    pragma_name = (
      pragma_match
      .group(1)
      .lower()
    )

    if pragma_name in SAFE_PRAGMAS:
      return True, None

    return (
      False,
      "That PRAGMA is not available."
    )

  return (
    False,
    "Read-only console: SELECT, WITH, "
    "safe PRAGMA and EXPLAIN QUERY PLAN only."
  )


def format_cell(value):
  if value is None:
    return None

  if isinstance(value, bytes):
    return value.hex()

  text = str(value)

  if len(text) > 500:
    return text[:500] + "..."

  return text


@app.route("/")
def index():
  return render_template(
    "index.html"
  )


@app.route("/health")
def health():
  return jsonify({
    "status": "ok"
  })


@app.route(
  "/api/query",
  methods=["POST"]
)
def run_query():
  body = request.get_json(
    silent=True
  ) or {}

  query = str(body.get("query", ""))
  valid, error = validate_query(query)

  if not valid:
    return jsonify({
      "ok": False,
      "error": error
    }), 400

  started = time.perf_counter()
  connection = None

  try:
    connection = get_connection()
    cursor = connection.execute(query)
    columns = []

    if cursor.description:
      columns = [
        item[0]
        for item in cursor.description
      ]

    rows = cursor.fetchmany(
      MAX_ROWS + 1
    )

    truncated = (
      len(rows) > MAX_ROWS
    )

    rows = rows[:MAX_ROWS]

    formatted_rows = [
      [
        format_cell(value)
        for value in row
      ]
      for row in rows
    ]

    elapsed = (
      time.perf_counter()
      - started
    ) * 1000

    return jsonify({
      "ok": True,
      "columns": columns,
      "rows": formatted_rows,
      "rowCount": len(formatted_rows),
      "truncated": truncated,
      "elapsedMs": round(
        elapsed,
        2
      )
    })

  except sqlite3.Error as exc:
    return jsonify({
      "ok": False,
      "error": str(exc)
    }), 400

  except Exception:
    return jsonify({
      "ok": False,
      "error": "Query execution failed."
    }), 500

  finally:
    if connection is not None:
      connection.close()


@app.route(
  "/api/unlock",
  methods=["POST"]
)
def unlock():
  body = request.get_json(
    silent=True
  ) or {}

  code = str(
    body.get("code", "")
  ).strip().upper()

  if code != UNLOCK_CODE:
    return jsonify({
      "ok": False,
      "message": "ACCESS DENIED"
    }), 403

  return jsonify({
    "ok": True,
    "message": "INCIDENT RESOLVED",
    "flag": FLAG
  })


if __name__ == "__main__":
  app.run(
    host="0.0.0.0",
    port=8000,
    debug=False
  )