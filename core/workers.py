from __future__ import annotations

import threading
from pathlib import Path
from typing import List

from PySide6.QtCore import QObject, QThread, Signal

from core.scanner import PDFScanner
from core.duplicate_detector import DuplicateDetector
from core.cache import PDFCache
from core.logger import PDFLogger
from core.merger import PDFMerger


class WorkerSignals(QObject):

    # Status
    status = Signal(str)
    error = Signal(str)
    finished = Signal()

    # Scan
    scan_started = Signal()
    scan_finished = Signal(list)

    # Progress
    overall_progress = Signal(int, int)
    folder_progress = Signal(str, int, int)
    current_file = Signal(str)

    # Merge
    merge_started = Signal(int)
    merge_finished = Signal(str)

    # Duplicate handling
    duplicates_found = Signal(list)


class MergeWorker(QThread):

    def __init__(
        self,
        folders: List[Path],
        output_file: Path,
    ):
        super().__init__()

        self.folders = folders
        self.output_file = output_file

        self.signals = WorkerSignals()

        self.scanner = PDFScanner()
        self.detector = DuplicateDetector()
        self.cache = PDFCache()
        self.logger = PDFLogger()

        self.merger = PDFMerger()

        self._pause = threading.Event()
        self._pause.set()

        self._cancel = False

        self.duplicate_action = None
        self.apply_to_all = False

    # -----------------------------------------------------

    def pause(self):
        self._pause.clear()

    # -----------------------------------------------------

    def resume(self):
        self._pause.set()

    # -----------------------------------------------------

    def cancel(self):

        self._cancel = True

        self._pause.set()

    # -----------------------------------------------------

    def set_duplicate_action(
        self,
        action,
        apply_to_all=False,
    ):

        self.duplicate_action = action
        self.apply_to_all = apply_to_all

        self.resume()

    # -----------------------------------------------------

    def check_cancel(self):

        if self._cancel:
            raise InterruptedError("Cancelled by user.")

    # -----------------------------------------------------

    def wait_if_paused(self):

        self._pause.wait()

        self.check_cancel()

    # -----------------------------------------------------

    def run(self):

        try:

            self.logger.start()

            self.signals.scan_started.emit()

            self.signals.status.emit(
                "Scanning folders..."
            )

            pdfs = self.scanner.scan(
                self.folders
            )

            self.signals.scan_finished.emit(
                pdfs
            )

            if not pdfs:

                self.signals.status.emit(
                    "No PDF files found."
                )

                return

            self.logger.scanned(
                len(pdfs)
            )

            self.check_cancel()

            self.signals.status.emit(
                "Checking duplicates..."
            )

            duplicate_groups = self.detector.scan(
                pdfs
            )

            if duplicate_groups:

                self.pause()

                self.signals.duplicates_found.emit(
                    duplicate_groups
                )

                self.wait_if_paused()

            merge_list = self._prepare_merge_list(
                pdfs,
                duplicate_groups,
            )

            self.check_cancel()

            self.signals.merge_started.emit(
                len(merge_list)
            )

            self.signals.status.emit(
                "Merging PDFs..."
            )
            folder_totals = {}

            folder_done = {}

            for pdf in merge_list:

                folder = str(pdf.parent)

                folder_totals.setdefault(folder, 0)
                folder_totals[folder] += 1

                folder_done.setdefault(folder, 0)

            total = len(merge_list)

            def progress_callback(index, count, pdf):

                self.wait_if_paused()

                folder = str(pdf.parent)

                folder_done[folder] += 1

                self.signals.current_file.emit(
                    str(pdf)
                )

                self.signals.folder_progress.emit(
                    folder,
                    folder_done[folder],
                    folder_totals[folder],
                )

                self.signals.overall_progress.emit(
                    index,
                    count,
                )

                self.logger.merged(pdf)

                self.check_cancel()

            self.merger.merge(
                merge_list,
                self.output_file,
                progress_callback,
            )

            self.logger.output(
                self.output_file
            )

            self.signals.merge_finished.emit(
                str(self.output_file)
            )

            self.signals.status.emit(
                "Merge completed."
            )

        except InterruptedError:

            self.signals.status.emit(
                "Operation cancelled."
            )

        except Exception as ex:

            self.logger.exception(ex)

            self.signals.error.emit(
                str(ex)
            )

        finally:

            self.cache.close()

            self.scanner.cleanup()

            self.logger.finish()

            self.logger.close()

            self.signals.finished.emit()

    # -----------------------------------------------------

    def _prepare_merge_list(
        self,
        pdfs,
        duplicate_groups,
    ):

        """
        Remove duplicate files depending upon
        the action selected by the user.
        """

        if not duplicate_groups:

            return sorted(pdfs)

        if self.duplicate_action is None:

            return sorted(pdfs)

        files = set(pdfs)

        #
        # KEEP ALL
        #

        if self.duplicate_action == 1:

            return sorted(files)

        #
        # KEEP ORIGINAL
        #

        if self.duplicate_action == 0:

            for group in duplicate_groups:

                for dup in group.duplicates:

                    if dup.path in files:

                        files.remove(
                            dup.path
                        )

                        self.logger.duplicate(
                            group.original.path,
                            dup.path,
                        )

            return sorted(files)

        #
        # SKIP DUPLICATES
        #

        if self.duplicate_action == 2:

            for group in duplicate_groups:

                if group.original.path in files:

                    files.remove(
                        group.original.path
                    )

                for dup in group.duplicates:

                    if dup.path in files:

                        files.remove(
                            dup.path
                        )

            return sorted(files)

        return sorted(files)
        # -----------------------------------------------------

    def update_duplicate_decision(
        self,
        action: int,
        apply_to_all: bool = False,
    ):
        """
        Called by the UI after the duplicate dialog closes.
        """

        self.duplicate_action = action
        self.apply_to_all = apply_to_all

        self.resume()

    # -----------------------------------------------------

    def build_cache(self, pdf_infos):

        """
        Save PDF metadata into SQLite cache.
        """

        for info in pdf_infos:

            try:
                self.cache.put(info)
            except Exception as ex:
                self.logger.warning(
                    f"Cache update failed: {info.path}"
                )
                self.logger.warning(str(ex))

    # -----------------------------------------------------

    def clear_cache(self):

        try:

            self.cache.clear()

            self.logger.info(
                "Metadata cache cleared."
            )

        except Exception as ex:

            self.logger.warning(str(ex))

    # -----------------------------------------------------

    def remove_missing_cache_entries(self):

        """
        Remove stale entries whose files
        no longer exist.
        """

        cursor = self.cache.conn.execute(
            "SELECT path FROM pdf_cache"
        )

        for row in cursor.fetchall():

            pdf = Path(row["path"])

            if not pdf.exists():

                self.cache.remove(pdf)

    # -----------------------------------------------------

    def emit_status(self, message: str):

        self.logger.info(message)

        self.signals.status.emit(message)

    # -----------------------------------------------------

    def emit_error(self, message: str):

        self.logger.error(message)

        self.signals.error.emit(message)

    # -----------------------------------------------------

    def is_cancelled(self) -> bool:

        return self._cancel

    # -----------------------------------------------------

    def reset(self):

        """
        Prepare worker for another run.
        """

        self._cancel = False

        self._pause.set()

        self.duplicate_action = None

        self.apply_to_all = False

    # -----------------------------------------------------

    def __del__(self):

        try:
            self.cache.close()
        except Exception:
            pass

        try:
            self.scanner.cleanup()
        except Exception:
            pass