from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime


class PDFLogger:

    def __init__(self, log_dir: Path = Path("logs")):

        log_dir.mkdir(parents=True, exist_ok=True)

        logfile = log_dir / (
            datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
        )

        self.logger = logging.getLogger("PDFMerger")

        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(
            logfile,
            encoding="utf-8",
        )

        console_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logfile = logfile

    # ---------------------------------------------------------

    def info(self, message: str):
        self.logger.info(message)

    # ---------------------------------------------------------

    def warning(self, message: str):
        self.logger.warning(message)

    # ---------------------------------------------------------

    def error(self, message: str):
        self.logger.error(message)

    # ---------------------------------------------------------

    def exception(self, ex: Exception):
        self.logger.exception(ex)

    # ---------------------------------------------------------

    def file(self) -> Path:
        return self.logfile

    # ---------------------------------------------------------

    def start(self):

        self.info("=" * 70)
        self.info("PDF Merge Started")
        self.info("=" * 70)

    # ---------------------------------------------------------

    def finish(self):

        self.info("=" * 70)
        self.info("PDF Merge Finished")
        self.info("=" * 70)

    # ---------------------------------------------------------

    def scanned(self, pdf_count: int):

        self.info(f"Scanned PDFs : {pdf_count}")

    # ---------------------------------------------------------

    def duplicate(self, original: Path, duplicate: Path):

        self.info(
            f"Duplicate: {duplicate} -> Original: {original}"
        )

    # ---------------------------------------------------------

    def merged(self, pdf: Path):

        self.info(f"Merged: {pdf}")

    # ---------------------------------------------------------

    def skipped(self, pdf: Path):

        self.info(f"Skipped: {pdf}")

    # ---------------------------------------------------------

    def output(self, pdf: Path):

        self.info(f"Output File: {pdf}")

    # ---------------------------------------------------------

    def close(self):

        logging.shutdown()