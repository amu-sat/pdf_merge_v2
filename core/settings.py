from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings


class Settings:

    ORGANIZATION = "PDFMerger"
    APPLICATION = "PDFMerger"

    def __init__(self):

        self.settings = QSettings(
            self.ORGANIZATION,
            self.APPLICATION,
        )

    # ---------------------------------------------------------
    # Last Used Paths
    # ---------------------------------------------------------

    def last_input_folder(self) -> str:
        return self.settings.value(
            "paths/input",
            str(Path.home()),
            type=str,
        )

    def set_last_input_folder(self, path: str):
        self.settings.setValue("paths/input", path)

    def last_output_folder(self) -> str:
        return self.settings.value(
            "paths/output",
            str(Path.home()),
            type=str,
        )

    def set_last_output_folder(self, path: str):
        self.settings.setValue("paths/output", path)

    # ---------------------------------------------------------
    # Merge Options
    # ---------------------------------------------------------

    def recursive(self) -> bool:
        return self.settings.value(
            "merge/recursive",
            True,
            type=bool,
        )

    def set_recursive(self, value: bool):
        self.settings.setValue("merge/recursive", value)

    def extract_archives(self) -> bool:
        return self.settings.value(
            "merge/extract_archives",
            True,
            type=bool,
        )

    def set_extract_archives(self, value: bool):
        self.settings.setValue(
            "merge/extract_archives",
            value,
        )

    def detect_duplicates(self) -> bool:
        return self.settings.value(
            "merge/detect_duplicates",
            True,
            type=bool,
        )

    def set_detect_duplicates(self, value: bool):
        self.settings.setValue(
            "merge/detect_duplicates",
            value,
        )

    def keep_bookmarks(self) -> bool:
        return self.settings.value(
            "merge/bookmarks",
            True,
            type=bool,
        )

    def set_keep_bookmarks(self, value: bool):
        self.settings.setValue(
            "merge/bookmarks",
            value,
        )

    # ---------------------------------------------------------
    # User Interface
    # ---------------------------------------------------------

    def theme(self) -> str:
        return self.settings.value(
            "ui/theme",
            "light",
            type=str,
        )

    def set_theme(self, theme: str):
        self.settings.setValue(
            "ui/theme",
            theme,
        )

    def window_geometry(self):
        return self.settings.value(
            "ui/geometry"
        )

    def set_window_geometry(self, geometry):
        self.settings.setValue(
            "ui/geometry",
            geometry,
        )

    def window_state(self):
        return self.settings.value(
            "ui/state"
        )

    def set_window_state(self, state):
        self.settings.setValue(
            "ui/state",
            state,
        )

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def enable_logging(self) -> bool:
        return self.settings.value(
            "logging/enabled",
            True,
            type=bool,
        )

    def set_enable_logging(self, value: bool):
        self.settings.setValue(
            "logging/enabled",
            value,
        )

    # ---------------------------------------------------------
    # Cache
    # ---------------------------------------------------------

    def enable_cache(self) -> bool:
        return self.settings.value(
            "cache/enabled",
            True,
            type=bool,
        )

    def set_enable_cache(self, value: bool):
        self.settings.setValue(
            "cache/enabled",
            value,
        )

    # ---------------------------------------------------------
    # Misc
    # ---------------------------------------------------------

    def clear(self):
        self.settings.clear()

    def sync(self):
        self.settings.sync()