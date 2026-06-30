from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from core.duplicate_detector import PDFInfo


class PDFCache:

    def __init__(self, db_path: Path = Path("cache.db")):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    # ---------------------------------------------------------

    def _create_table(self):

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pdf_cache
            (
                path TEXT PRIMARY KEY,
                size INTEGER NOT NULL,
                mtime REAL NOT NULL,
                pages INTEGER NOT NULL,
                sha256 TEXT NOT NULL
            )
            """
        )

        self.conn.commit()

    # ---------------------------------------------------------

    def get(self, pdf: Path) -> Optional[PDFInfo]:

        cursor = self.conn.execute(
            """
            SELECT *
            FROM pdf_cache
            WHERE path=?
            """,
            (str(pdf),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        try:
            stat = pdf.stat()
        except Exception:
            return None

        if (
            stat.st_size != row["size"]
            or stat.st_mtime != row["mtime"]
        ):
            return None

        return PDFInfo(
            path=pdf,
            size=row["size"],
            pages=row["pages"],
            sha256=row["sha256"],
        )

    # ---------------------------------------------------------

    def put(self, info: PDFInfo):

        stat = info.path.stat()

        self.conn.execute(
            """
            INSERT OR REPLACE INTO pdf_cache
            (
                path,
                size,
                mtime,
                pages,
                sha256
            )
            VALUES (?, ?, ?, ?, ?)
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

    # ---------------------------------------------------------

    def remove(self, pdf: Path):

        self.conn.execute(
            """
            DELETE FROM pdf_cache
            WHERE path=?
            """,
            (str(pdf),),
        )

        self.conn.commit()

    # ---------------------------------------------------------

    def clear(self):

        self.conn.execute(
            """
            DELETE FROM pdf_cache
            """
        )

        self.conn.commit()

    # ---------------------------------------------------------

    def vacuum(self):

        self.conn.execute("VACUUM")
        self.conn.commit()

    # ---------------------------------------------------------

    def close(self):

        self.conn.close()