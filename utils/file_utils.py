from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterable, List


def ensure_directory(path: Path) -> Path:
    """
    Create directory if it does not exist.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------


def create_temp_directory(prefix: str = "pdfmerge_") -> Path:
    """
    Create temporary directory.
    """
    return Path(tempfile.mkdtemp(prefix=prefix))


# ---------------------------------------------------------


def remove_directory(path: Path):

    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


# ---------------------------------------------------------


def pdf_files(folder: Path, recursive: bool = True) -> List[Path]:

    if recursive:
        files = folder.rglob("*.pdf")
    else:
        files = folder.glob("*.pdf")

    return sorted(
        [
            f
            for f in files
            if f.is_file()
        ]
    )


# ---------------------------------------------------------


def archive_files(folder: Path, recursive: bool = True) -> List[Path]:

    extensions = {
        ".zip",
        ".rar",
        ".7z",
    }

    iterator = folder.rglob("*") if recursive else folder.glob("*")

    return sorted(
        [
            f
            for f in iterator
            if f.is_file()
            and f.suffix.lower() in extensions
        ]
    )


# ---------------------------------------------------------


def unique_paths(paths: Iterable[Path]) -> List[Path]:

    return sorted(
        list(
            {
                p.resolve()
                for p in paths
            }
        )
    )


# ---------------------------------------------------------


def file_size(path: Path) -> int:

    return path.stat().st_size


# ---------------------------------------------------------


def total_size(paths: Iterable[Path]) -> int:

    return sum(
        p.stat().st_size
        for p in paths
        if p.exists()
    )


# ---------------------------------------------------------


def human_size(size: int) -> str:

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


# ---------------------------------------------------------


def relative_path(path: Path, root: Path) -> Path:

    try:
        return path.relative_to(root)

    except Exception:
        return path


# ---------------------------------------------------------


def safe_delete(path: Path):

    try:

        if path.exists():
            path.unlink()

    except Exception:
        pass


# ---------------------------------------------------------


def copy_file(
    source: Path,
    destination: Path,
):

    ensure_directory(destination.parent)

    shutil.copy2(source, destination)


# ---------------------------------------------------------


def move_file(
    source: Path,
    destination: Path,
):

    ensure_directory(destination.parent)

    shutil.move(str(source), str(destination))


# ---------------------------------------------------------


def filename_without_extension(path: Path) -> str:

    return path.stem


# ---------------------------------------------------------


def extension(path: Path) -> str:

    return path.suffix.lower()