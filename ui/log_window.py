from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LogWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Log Viewer")
        self.resize(800, 500)

        self._build_ui()

    # ---------------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        layout.addWidget(self.editor)

        buttons = QHBoxLayout()

        self.clear_btn = QPushButton("Clear")
        self.save_btn = QPushButton("Save")
        self.load_btn = QPushButton("Open Log")
        self.close_btn = QPushButton("Close")

        buttons.addWidget(self.clear_btn)
        buttons.addWidget(self.load_btn)
        buttons.addWidget(self.save_btn)

        buttons.addStretch()

        buttons.addWidget(self.close_btn)

        layout.addLayout(buttons)

        self.clear_btn.clicked.connect(self.clear)

        self.save_btn.clicked.connect(self.save_log)

        self.load_btn.clicked.connect(self.load_log)

        self.close_btn.clicked.connect(self.close)

    # ---------------------------------------------------------

    def append(self, text: str):

        self.editor.append(text)

        cursor = self.editor.textCursor()

        cursor.movePosition(QTextCursor.End)

        self.editor.setTextCursor(cursor)

    # ---------------------------------------------------------

    def append_lines(self, lines):

        for line in lines:
            self.append(line)

    # ---------------------------------------------------------

    def clear(self):

        self.editor.clear()

    # ---------------------------------------------------------

    def text(self):

        return self.editor.toPlainText()

    # ---------------------------------------------------------

    def set_text(self, text: str):

        self.editor.setPlainText(text)

    # ---------------------------------------------------------

    def load_log(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Log",
            "",
            "Log Files (*.log);;Text Files (*.txt)",
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "r",
                encoding="utf-8",
            ) as f:

                self.editor.setPlainText(
                    f.read()
                )

        except Exception as ex:

            self.append(
                f"Error opening file:\n{ex}"
            )

    # ---------------------------------------------------------

    def save_log(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log",
            "merge.log",
            "Log Files (*.log)",
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(
                    self.editor.toPlainText()
                )

        except Exception as ex:

            self.append(
                f"Error saving file:\n{ex}"
            )

    # ---------------------------------------------------------

    def load_from_file(
        self,
        logfile: Path,
    ):

        if not logfile.exists():
            return

        try:

            with logfile.open(
                "r",
                encoding="utf-8",
            ) as f:

                self.editor.setPlainText(
                    f.read()
                )

        except Exception as ex:

            self.append(str(ex))

    # ---------------------------------------------------------

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close()
            return

        super().keyPressEvent(event)