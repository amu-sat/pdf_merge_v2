from __future__ import annotations

import sqlite3
from pathlib import Path

from core.duplicate_detector import PDFInfo


class PDFCache:

    def __init__(self, db_path: Path = Path("cache.db")):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS pdf_cache
        (
            path TEXT PRIMARY KEY,
            size INTEGER,
            mtime REAL,
            pages INTEGER,
            sha256 TEXT
        )
        """)

        self.conn.commit()

    def put(self, info: PDFInfo):

        stat = info.path.stat()

        self.conn.execute(
            """
            INSERT OR REPLACE INTO pdf_cache
            VALUES (?,?,?,?,?)
            """,
            (
                str(info.path),
                stat.st_size,
                stat.st_mtime,
                info.pages,
                info.sha256,
            ),
        )

        self.conn.commit()

    def get(self, pdf: Path):

        cur = self.conn.execute(
            "SELECT * FROM pdf_cache WHERE path=?",
            (str(pdf),),
        )

        return cur.fetchone()

    def remove(self, pdf: Path):

        self.conn.execute(
            "DELETE FROM pdf_cache WHERE path=?",
            (str(pdf),),
        )

        self.conn.commit()

    def clear(self):

        self.conn.execute(
            "DELETE FROM pdf_cache"
        )

        self.conn.commit()

    def close(self):

        self.conn.close()