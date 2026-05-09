import sqlite3

def connect() -> sqlite3.Connection:
    conn = sqlite3.connect("./todos.db")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS todos "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)"
    )
    conn.commit()
    return conn

def row_to_dict(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
