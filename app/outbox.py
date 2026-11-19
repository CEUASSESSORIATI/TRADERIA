import json
import sqlite3
from pathlib import Path
from typing import Any


class Outbox:
    """Durable local delivery queue only; not the business database."""

    def __init__(self, path: Path) -> None:
        self.path = path
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS outbox (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def enqueue(self, event_type: str, payload: dict[str, Any]) -> None:
        with self._connect() as db:
            db.execute("INSERT INTO outbox(event_type, payload) VALUES (?, ?)",
                       (event_type, json.dumps(payload, ensure_ascii=False)))

    def pending(self, limit: int = 100) -> list[tuple[int, str, dict[str, Any]]]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, event_type, payload FROM outbox ORDER BY id LIMIT ?", (limit,)
            ).fetchall()
        return [(row[0], row[1], json.loads(row[2])) for row in rows]

    def acknowledge(self, event_id: int) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM outbox WHERE id = ?", (event_id,))

    def count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0])
