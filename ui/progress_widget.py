from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QScrollArea,
    QFrame,
)


class FolderProgress(QFrame):

    def __init__(self, folder: str):
        super().__init__()

        self.folder = folder

        layout = QVBoxLayout(self)

        self.label = QLabel(folder)

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)

        self.status = QLabel("0 / 0")

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)

    # -----------------------------------------------------

    def update_progress(self, current: int, total: int):

        if total == 0:
            percent = 0
        else:
            percent = int(current * 100 / total)

        self.progress.setValue(percent)
        self.status.setText(f"{current} / {total}")


class ProgressWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.folder_widgets = {}

        layout = QVBoxLayout(self)

        self.current_file = QLabel("")

        self.overall = QProgressBar()
        self.overall.setMinimum(0)
        self.overall.setMaximum(100)

        self.overall_status = QLabel("0 / 0")

        layout.addWidget(QLabel("Overall Progress"))
        layout.addWidget(self.overall)
        layout.addWidget(self.overall_status)
        layout.addWidget(self.current_file)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.folder_layout = QVBoxLayout(self.container)

        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)

    # -----------------------------------------------------

    def add_folder(self, folder: str):

        if folder in self.folder_widgets:
            return

        widget = FolderProgress(folder)

        self.folder_layout.addWidget(widget)

        self.folder_widgets[folder] = widget

    # -----------------------------------------------------

    def update_folder(self, folder: str, current: int, total: int):

        if folder not in self.folder_widgets:
            self.add_folder(folder)

        self.folder_widgets[folder].update_progress(current, total)

    # -----------------------------------------------------

    def update_overall(self, current: int, total: int):

        if total == 0:
            percent = 0
        else:
            percent = int(current * 100 / total)

        self.overall.setValue(percent)
        self.overall_status.setText(f"{current} / {total}")

    # -----------------------------------------------------

    def set_current_file(self, filename: str):

        self.current_file.setText(filename)

    # -----------------------------------------------------

    def reset(self):

        self.overall.setValue(0)
        self.overall_status.setText("0 / 0")
        self.current_file.setText("")

        while self.folder_layout.count():

            item = self.folder_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.folder_widgets.clear()