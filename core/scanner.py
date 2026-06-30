from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

try:
    import py7zr
except ImportError:
    py7zr = None

try:
    import rarfile
except ImportError:
    rarfile = None


PDF_EXT = ".pdf"
ZIP_EXT = ".zip"
RAR_EXT = ".rar"
SEVENZ_EXT = ".7z"


@dataclass
class FolderInfo:
    folder: Path
    pdfs: List[Path] = field(default_factory=list)
    archives: List[Path] = field(default_factory=list)


class PDFScanner:
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="pdfmerge_"))
        self.folders: List[FolderInfo] = []

    # --------------------------------------------------------

    def scan(self, folders: List[Path]) -> List[Path]:
        """
        Scan folders recursively.

        Returns:
            List[Path] : All discovered PDFs.
        """

        self.folders.clear()

        all_pdfs = []

        for folder in folders:

            info = FolderInfo(folder=folder)

            # Find archives
            for ext in (ZIP_EXT, RAR_EXT, SEVENZ_EXT):
                info.archives.extend(folder.rglob(f"*{ext}"))

            # Extract archives
            for archive in info.archives:
                self._extract_archive(archive)

            # Find PDFs
            info.pdfs.extend(self.temp_dir.rglob("*.pdf"))
            info.pdfs.extend(folder.rglob("*.pdf"))

            info.pdfs = sorted(set(info.pdfs))

            self.folders.append(info)

            all_pdfs.extend(info.pdfs)

        return sorted(set(all_pdfs))

    # --------------------------------------------------------

    def folder_statistics(self):

        stats = []

        for folder in self.folders:

            stats.append(
                {
                    "folder": folder.folder,
                    "pdf_count": len(folder.pdfs),
                    "archive_count": len(folder.archives),
                }
            )

        return stats

    # --------------------------------------------------------

    def _extract_archive(self, archive: Path):

        destination = self.temp_dir / archive.stem
        destination.mkdir(parents=True, exist_ok=True)

        suffix = archive.suffix.lower()

        try:

            if suffix == ZIP_EXT:

                with zipfile.ZipFile(archive, "r") as zf:
                    zf.extractall(destination)

            elif suffix == RAR_EXT and rarfile is not None:

                with rarfile.RarFile(archive) as rf:
                    rf.extractall(destination)

            elif suffix == SEVENZ_EXT and py7zr is not None:

                with py7zr.SevenZipFile(archive, "r") as sz:
                    sz.extractall(destination)

        except Exception as e:
            print(f"Archive extraction failed: {archive}")
            print(e)

    # --------------------------------------------------------

    def cleanup(self):

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)