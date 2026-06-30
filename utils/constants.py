from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

APP_NAME = "PDF Merger"

APP_VERSION = "1.0.0"

ORGANIZATION = "PDFMerger"

# ---------------------------------------------------------
# Supported Files
# ---------------------------------------------------------

PDF_EXTENSION = ".pdf"

SUPPORTED_ARCHIVES = [
    ".zip",
    ".rar",
    ".7z",
]

SUPPORTED_PDF = [
    ".pdf",
]

# ---------------------------------------------------------
# Default Paths
# ---------------------------------------------------------

HOME_DIR = Path.home()

OUTPUT_FILENAME = "merged.pdf"

CACHE_DATABASE = "cache.db"

LOG_DIRECTORY = "logs"

TEMP_DIRECTORY = "temp"

OUTPUT_DIRECTORY = "output"

# ---------------------------------------------------------
# Merge Options
# ---------------------------------------------------------

DEFAULT_RECURSIVE = True

DEFAULT_DETECT_DUPLICATES = True

DEFAULT_EXTRACT_ARCHIVES = True

DEFAULT_KEEP_BOOKMARKS = True

DEFAULT_ENABLE_CACHE = True

DEFAULT_ENABLE_LOGGING = True

# ---------------------------------------------------------
# Duplicate Actions
# ---------------------------------------------------------

KEEP_ORIGINAL = 0

KEEP_ALL = 1

SKIP_DUPLICATES = 2

CANCEL = 3

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

WINDOW_WIDTH = 1200

WINDOW_HEIGHT = 750

PROGRESS_UPDATE_INTERVAL = 100

# ---------------------------------------------------------
# Buffer Sizes
# ---------------------------------------------------------

HASH_BUFFER_SIZE = 1024 * 1024  # 1 MB

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(message)s"
)

LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ---------------------------------------------------------
# Archive Filters
# ---------------------------------------------------------

ARCHIVE_FILTER = (
    "*.zip *.ZIP "
    "*.rar *.RAR "
    "*.7z *.7Z"
)

# ---------------------------------------------------------
# File Dialog Filters
# ---------------------------------------------------------

PDF_FILTER = "PDF Files (*.pdf)"

LOG_FILTER = "Log Files (*.log)"

OUTPUT_FILTER = "PDF Files (*.pdf)"

# ---------------------------------------------------------
# Status Messages
# ---------------------------------------------------------

STATUS_READY = "Ready"

STATUS_SCANNING = "Scanning folders..."

STATUS_DUPLICATES = "Checking duplicate PDFs..."

STATUS_MERGING = "Merging PDFs..."

STATUS_FINISHED = "Completed"

STATUS_CANCELLED = "Cancelled"

STATUS_ERROR = "Error"

# ---------------------------------------------------------
# Icons (future use)
# ---------------------------------------------------------

ICON_APP = "resources/icon.ico"

STYLE_FILE = "resources/style.qss"