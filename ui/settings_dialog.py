from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QCheckBox,
    QComboBox,
    QPushButton,
)

from core.settings import Settings


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = Settings()

        self.setWindowTitle("Settings")
        self.resize(450, 350)

        self.build_ui()
        self.load_settings()

    # ---------------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(self)

        # ---------------------------------------------
        # Merge
        # ---------------------------------------------

        merge_group = QGroupBox("Merge Options")

        merge_layout = QVBoxLayout(merge_group)

        self.recursive = QCheckBox("Scan folders recursively")

        self.extract_archives = QCheckBox(
            "Extract ZIP / RAR / 7Z archives"
        )

        self.detect_duplicates = QCheckBox(
            "Detect duplicate PDFs"
        )

        self.keep_bookmarks = QCheckBox(
            "Generate bookmarks"
        )

        merge_layout.addWidget(self.recursive)
        merge_layout.addWidget(self.extract_archives)
        merge_layout.addWidget(self.detect_duplicates)
        merge_layout.addWidget(self.keep_bookmarks)

        layout.addWidget(merge_group)

        # ---------------------------------------------
        # Performance
        # ---------------------------------------------

        performance_group = QGroupBox("Performance")

        performance_layout = QVBoxLayout(
            performance_group
        )

        self.enable_cache = QCheckBox(
            "Enable SQLite metadata cache"
        )

        self.enable_logging = QCheckBox(
            "Enable logging"
        )

        performance_layout.addWidget(
            self.enable_cache
        )

        performance_layout.addWidget(
            self.enable_logging
        )

        layout.addWidget(performance_group)

        # ---------------------------------------------
        # Theme
        # ---------------------------------------------

        appearance_group = QGroupBox("Appearance")

        appearance_layout = QVBoxLayout(
            appearance_group
        )

        self.theme = QComboBox()

        self.theme.addItems(
            [
                "light",
                "dark",
            ]
        )

        appearance_layout.addWidget(self.theme)

        layout.addWidget(appearance_group)

        # ---------------------------------------------
        # Buttons
        # ---------------------------------------------

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")

        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addLayout(buttons)

        self.ok_btn.clicked.connect(self.accept_settings)
        self.cancel_btn.clicked.connect(self.reject)

    # ---------------------------------------------------------

    def load_settings(self):

        self.recursive.setChecked(
            self.settings.recursive()
        )

        self.extract_archives.setChecked(
            self.settings.extract_archives()
        )

        self.detect_duplicates.setChecked(
            self.settings.detect_duplicates()
        )

        self.keep_bookmarks.setChecked(
            self.settings.keep_bookmarks()
        )

        self.enable_cache.setChecked(
            self.settings.enable_cache()
        )

        self.enable_logging.setChecked(
            self.settings.enable_logging()
        )

        index = self.theme.findText(
            self.settings.theme()
        )

        if index >= 0:
            self.theme.setCurrentIndex(index)

    # ---------------------------------------------------------

    def accept_settings(self):

        self.settings.set_recursive(
            self.recursive.isChecked()
        )

        self.settings.set_extract_archives(
            self.extract_archives.isChecked()
        )

        self.settings.set_detect_duplicates(
            self.detect_duplicates.isChecked()
        )

        self.settings.set_keep_bookmarks(
            self.keep_bookmarks.isChecked()
        )

        self.settings.set_enable_cache(
            self.enable_cache.isChecked()
        )

        self.settings.set_enable_logging(
            self.enable_logging.isChecked()
        )

        self.settings.set_theme(
            self.theme.currentText()
        )

        self.settings.sync()

        self.accept()