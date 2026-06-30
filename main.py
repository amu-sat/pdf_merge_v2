from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("PDF Merger")
    app.setOrganizationName("PDFMerger")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()