from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSplitter,
    QToolBar,
    QStatusBar,
    QMenuBar,
    QApplication,
)

from core.workers import MergeWorker
from core.settings import Settings
from core.logger import PDFLogger
from ui.progress_widget import ProgressWidget
from ui.duplicate_dialog import DuplicateDialog


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.settings = Settings()
        self.logger = PDFLogger()

        self.worker = None

        self.input_folders = []
        self.output_pdf = None

        self.setWindowTitle("PDF Merger")
        self.resize(1200, 750)

        geometry = self.settings.window_geometry()
        if geometry:
            self.restoreGeometry(geometry)

        self._create_menu()
        self._create_toolbar()
        self._create_statusbar()
        self._create_ui()

        self.setAcceptDrops(True)

    # ---------------------------------------------------------

    def _create_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)

        root.addWidget(splitter)

        # -------------------------------------------------
        # LEFT PANEL
        # -------------------------------------------------

        left = QWidget()

        left_layout = QVBoxLayout(left)

        left_layout.addWidget(QLabel("Folders"))

        self.folder_list = QListWidget()

        left_layout.addWidget(self.folder_list)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add")

        self.remove_btn = QPushButton("Remove")

        self.clear_btn = QPushButton("Clear")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.clear_btn)

        left_layout.addLayout(btn_layout)

        splitter.addWidget(left)

        # -------------------------------------------------
        # RIGHT PANEL
        # -------------------------------------------------

        right = QWidget()

        right_layout = QVBoxLayout(right)

        output_layout = QHBoxLayout()

        self.output_edit = QLineEdit()

        self.output_btn = QPushButton("Browse")

        output_layout.addWidget(QLabel("Output"))

        output_layout.addWidget(self.output_edit)

        output_layout.addWidget(self.output_btn)

        right_layout.addLayout(output_layout)

        self.progress = ProgressWidget()

        right_layout.addWidget(self.progress)

        right_layout.addWidget(QLabel("Log"))

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        right_layout.addWidget(self.log)

        action_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start")

        self.pause_btn = QPushButton("Pause")

        self.resume_btn = QPushButton("Resume")

        self.cancel_btn = QPushButton("Cancel")

        action_layout.addWidget(self.start_btn)
        action_layout.addWidget(self.pause_btn)
        action_layout.addWidget(self.resume_btn)
        action_layout.addWidget(self.cancel_btn)

        right_layout.addLayout(action_layout)

        splitter.addWidget(right)

        splitter.setSizes([350, 850])

        # -------------------------------------------------

        self.add_btn.clicked.connect(self.add_folder)

        self.remove_btn.clicked.connect(self.remove_folder)

        self.clear_btn.clicked.connect(self.clear_folders)

        self.output_btn.clicked.connect(self.select_output)

        self.start_btn.clicked.connect(self.start_merge)

        self.pause_btn.clicked.connect(self.pause_merge)

        self.resume_btn.clicked.connect(self.resume_merge)

        self.cancel_btn.clicked.connect(self.cancel_merge)

    # ---------------------------------------------------------

    def _create_toolbar(self):

        toolbar = QToolBar()

        self.addToolBar(toolbar)

        toolbar.addWidget(self.add_btn if hasattr(self, "add_btn") else QLabel())

    # ---------------------------------------------------------

    def _create_menu(self):

        menubar = QMenuBar()

        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("&File")

        file_menu.addAction("Add Folder", self.add_folder)

        file_menu.addAction("Select Output", self.select_output)

        file_menu.addSeparator()

        file_menu.addAction("Exit", self.close)

    # ---------------------------------------------------------

    def _create_statusbar(self):

        status = QStatusBar()

        self.setStatusBar(status)

        status.showMessage("Ready")

    # ---------------------------------------------------------

    def log_message(self, message):

        self.log.append(message)

        self.logger.info(message)

        self.statusBar().showMessage(message)

    # ---------------------------------------------------------

    def add_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            self.settings.last_input_folder(),
        )

        if not folder:
            return

        folder = str(Path(folder))

        if folder not in self.input_folders:

            self.input_folders.append(folder)

            self.folder_list.addItem(folder)

            self.settings.set_last_input_folder(folder)

            self.log_message(f"Added folder: {folder}")

    # ---------------------------------------------------------

    def remove_folder(self):

        row = self.folder_list.currentRow()

        if row < 0:
            return

        self.input_folders.pop(row)

        self.folder_list.takeItem(row)

    # ---------------------------------------------------------

    def clear_folders(self):

        self.input_folders.clear()

        self.folder_list.clear()

        self.progress.reset()

    # ---------------------------------------------------------

    def select_output(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output PDF",
            str(
                Path(
                    self.settings.last_output_folder()
                ) / "merged.pdf"
            ),
            "PDF Files (*.pdf)",
        )

        if not filename:
            return

        self.output_pdf = Path(filename)

        self.output_edit.setText(str(self.output_pdf))

        self.settings.set_last_output_folder(
            str(self.output_pdf.parent)
        )

    # ---------------------------------------------------------

    def start_merge(self):

        if not self.input_folders:

            QMessageBox.warning(
                self,
                "No Folder",
                "Please add at least one folder.",
            )

            return

        if not self.output_edit.text():

            QMessageBox.warning(
                self,
                "Output Missing",
                "Please select an output PDF.",
            )

            return

        self.progress.reset()

        self.log.clear()

        self.logger.start()

        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        folders = [
            Path(folder)
            for folder in self.input_folders
        ]

        self.worker = MergeWorker(folders)

        self.worker.signals.scan_started.connect(
            self.on_scan_started
        )

        self.worker.signals.scan_finished.connect(
            self.on_scan_finished
        )

        self.worker.signals.folder_progress.connect(
            self.on_folder_progress
        )

        self.worker.signals.overall_progress.connect(
            self.on_overall_progress
        )

        self.worker.signals.current_file.connect(
            self.on_current_file
        )

        self.worker.signals.status.connect(
            self.on_status
        )

        self.worker.signals.error.connect(
            self.on_error
        )

        self.worker.signals.finished.connect(
            self.on_finished
        )

        self.worker.signals.duplicates_found.connect(
            self.on_duplicates
        )

        self.worker.start()

    # ---------------------------------------------------------

    def pause_merge(self):

        if self.worker is None:
            return

        self.worker.pause()

        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)

        self.log_message("Paused.")

    # ---------------------------------------------------------

    def resume_merge(self):

        if self.worker is None:
            return

        self.worker.resume()

        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)

        self.log_message("Resumed.")

    # ---------------------------------------------------------

    def cancel_merge(self):

        if self.worker is None:
            return

        self.worker.cancel()

        self.log_message("Cancelling...")

    # ---------------------------------------------------------

    def on_scan_started(self):

        self.log_message("Scanning folders...")

    # ---------------------------------------------------------

    def on_scan_finished(self, pdfs):

        self.log_message(
            f"{len(pdfs)} PDF(s) found."
        )

    # ---------------------------------------------------------

    def on_folder_progress(
        self,
        folder,
        current,
        total,
    ):

        self.progress.update_folder(
            folder,
            current,
            total,
        )

    # ---------------------------------------------------------

    def on_overall_progress(
        self,
        current,
        total,
    ):

        self.progress.update_overall(
            current,
            total,
        )

    # ---------------------------------------------------------

    def on_current_file(
        self,
        filename,
    ):

        self.progress.set_current_file(
            filename
        )

        self.statusBar().showMessage(
            Path(filename).name
        )

    # ---------------------------------------------------------

    def on_status(self, message):

        self.log_message(message)

    # ---------------------------------------------------------

    def on_error(self, message):

        QMessageBox.critical(
            self,
            "Error",
            message,
        )

        self.log_message(message)
        
    # ---------------------------------------------------------

    def on_duplicates(self, duplicate_groups):

        if not duplicate_groups:

            self.log_message("No duplicate PDFs found.")
            return

        self.log_message(
            f"{len(duplicate_groups)} duplicate group(s) found."
        )

        # Pause worker while user decides
        if self.worker:
            self.worker.pause()

        dialog = DuplicateDialog(
            duplicate_groups,
            self,
        )

        if dialog.exec():

            action = dialog.result_action
            apply_all = dialog.apply_to_all()

            self.log_message(
                f"Duplicate action: {action} "
                f"(Apply to all = {apply_all})"
            )

            # TODO:
            # Send duplicate handling decision back to worker.
            # Worker will remove skipped files before merge.

        else:

            if self.worker:
                self.worker.cancel()

            self.log_message(
                "Operation cancelled by user."
            )

            return

        if self.worker:
            self.worker.resume()

    # ---------------------------------------------------------

    def on_finished(self):

        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

        self.statusBar().showMessage(
            "Ready"
        )

        self.logger.finish()

        self.log_message(
            "Finished."
        )

    # ---------------------------------------------------------

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # ---------------------------------------------------------

    def dragMoveEvent(self, event):

        event.acceptProposedAction()

    # ---------------------------------------------------------

    def dropEvent(self, event):

        for url in event.mimeData().urls():

            path = Path(url.toLocalFile())

            if not path.exists():
                continue

            if path.is_dir():

                folder = str(path)

                if folder not in self.input_folders:

                    self.input_folders.append(folder)

                    self.folder_list.addItem(folder)

                    self.log_message(
                        f"Added folder: {folder}"
                    )

            elif path.is_file():

                if path.suffix.lower() == ".pdf":

                    folder = str(path.parent)

                    if folder not in self.input_folders:

                        self.input_folders.append(folder)

                        self.folder_list.addItem(folder)

                        self.log_message(
                            f"Added folder: {folder}"
                        )

    # ---------------------------------------------------------

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Delete:

            self.remove_folder()

            return

        super().keyPressEvent(event)

    # ---------------------------------------------------------

    def resizeEvent(self, event):

        super().resizeEvent(event)

    # ---------------------------------------------------------

    def moveEvent(self, event):

        super().moveEvent(event)

    # ---------------------------------------------------------

    def showEvent(self, event):

        super().showEvent(event)

        self.statusBar().showMessage(
            "Ready"
        )    
    # ---------------------------------------------------------

    def enable_controls(self, enabled: bool):

        self.add_btn.setEnabled(enabled)
        self.remove_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.output_btn.setEnabled(enabled)

    # ---------------------------------------------------------

    def reset_ui(self):

        self.progress.reset()

        self.statusBar().showMessage("Ready")

        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

    # ---------------------------------------------------------

    def clear_log(self):

        self.log.clear()

    # ---------------------------------------------------------

    def save_settings(self):

        self.settings.set_window_geometry(
            self.saveGeometry()
        )

        self.settings.set_window_state(
            self.saveState()
        )

        self.settings.sync()

    # ---------------------------------------------------------

    def restore_settings(self):

        geometry = self.settings.window_geometry()

        if geometry:
            self.restoreGeometry(geometry)

        state = self.settings.window_state()

        if state:
            self.restoreState(state)

    # ---------------------------------------------------------

    def closeEvent(self, event):

        if self.worker is not None:

            if self.worker.isRunning():

                reply = QMessageBox.question(
                    self,
                    "Exit",
                    "A merge operation is still running.\n"
                    "Do you want to cancel it and exit?",
                    QMessageBox.Yes | QMessageBox.No,
                )

                if reply == QMessageBox.No:
                    event.ignore()
                    return

                self.worker.cancel()

                self.worker.wait()

        self.save_settings()

        self.logger.close()

        event.accept()

    # ---------------------------------------------------------

    def append_log(self, text: str):

        self.log.append(text)

    # ---------------------------------------------------------

    def set_status(self, text: str):

        self.statusBar().showMessage(text)

    # ---------------------------------------------------------

    def information(
        self,
        title: str,
        message: str,
    ):

        QMessageBox.information(
            self,
            title,
            message,
        )

    # ---------------------------------------------------------

    def warning(
        self,
        title: str,
        message: str,
    ):

        QMessageBox.warning(
            self,
            title,
            message,
        )

    # ---------------------------------------------------------

    def critical(
        self,
        title: str,
        message: str,
    ):

        QMessageBox.critical(
            self,
            title,
            message,
        )

    # ---------------------------------------------------------

    def about(self):

        QMessageBox.about(
            self,
            "About",
            (
                "PDF Merger\n\n"
                "Version 1.0\n\n"
                "Features:\n"
                "• Recursive folder scanning\n"
                "• ZIP/RAR/7Z extraction\n"
                "• Duplicate PDF detection\n"
                "• Per-folder progress\n"
                "• Overall progress\n"
                "• Pause / Resume / Cancel\n"
                "• Automatic bookmarks\n"
                "• Logging\n"
                "• SQLite metadata cache"
            ),
        )