# PDF Merger

A Windows desktop application built with **Python** and **PySide6** for recursively scanning folders, extracting archives, detecting duplicate PDFs, and merging documents into a single PDF.

---

## Features

* Recursive folder scanning
* Merge multiple PDFs into a single document
* Automatic bookmark generation
* Duplicate PDF detection

  * File size
  * Page count
  * SHA-256 verification
* ZIP archive extraction
* RAR archive extraction *(requires UnRAR or 7-Zip)*
* 7Z archive extraction
* Per-folder progress bars
* Overall progress bar
* Pause / Resume / Cancel
* SQLite metadata cache
* Detailed logging
* Drag & Drop support

---

## Project Structure

```text
pdf_merger/
│
├── main.py
├── requirements.txt
│
├── core/
│   ├── scanner.py
│   ├── duplicate_detector.py
│   ├── merger.py
│   ├── workers.py
│   ├── bookmarks.py
│   ├── cache.py
│   ├── logger.py
│   └── settings.py
│
├── ui/
│   ├── main_window.py
│   ├── progress_widget.py
│   ├── duplicate_dialog.py
│   ├── settings_dialog.py
│   └── log_window.py
│
├── utils/
│   ├── constants.py
│   ├── file_utils.py
│   ├── hash_utils.py
│   └── pdf_utils.py
│
├── resources/
├── tests/
└── .github/
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running

```bash
python main.py
```

---

## Building an Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon resources/icon.ico ^
    main.py
```

The executable will be created inside:

```text
dist/
```

---

## Supported File Types

### PDF

* `.pdf`

### Archives

* `.zip`
* `.rar`
* `.7z`

---

## Duplicate Detection Workflow

1. Compare file size.
2. Compare page count.
3. Compare SHA-256 hash.
4. Ask the user how duplicates should be handled.
5. Merge the remaining files.

---

## Technologies Used

* Python 3.11+
* PySide6
* PyMuPDF
* SQLite
* py7zr
* rarfile

---

## Future Improvements

* PDF thumbnails
* Password-protected PDF support
* OCR support
* Watch folders
* Incremental merge
* Merge presets
* Batch processing
* Multi-core hashing
* Dark theme
* Automatic updates

---

## License

MIT License
