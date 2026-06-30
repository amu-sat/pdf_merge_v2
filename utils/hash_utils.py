from __future__ import annotations

import hashlib
from pathlib import Path

BUFFER_SIZE = 1024 * 1024  # 1 MB


# ---------------------------------------------------------


def sha256(file: Path) -> str:
    """
    Calculate SHA-256 hash.
    """

    h = hashlib.sha256()

    with file.open("rb") as f:

        while True:

            chunk = f.read(BUFFER_SIZE)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


# ---------------------------------------------------------


def md5(file: Path) -> str:
    """
    Calculate MD5 hash.
    """

    h = hashlib.md5()

    with file.open("rb") as f:

        while True:

            chunk = f.read(BUFFER_SIZE)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


# ---------------------------------------------------------


def sha1(file: Path) -> str:
    """
    Calculate SHA-1 hash.
    """

    h = hashlib.sha1()

    with file.open("rb") as f:

        while True:

            chunk = f.read(BUFFER_SIZE)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


# ---------------------------------------------------------


def compare(file1: Path, file2: Path) -> bool:
    """
    Compare two files using SHA-256.
    """

    if not file1.exists() or not file2.exists():
        return False

    if file1.stat().st_size != file2.stat().st_size:
        return False

    return sha256(file1) == sha256(file2)


# ---------------------------------------------------------


def verify(file: Path, expected_hash: str) -> bool:
    """
    Verify SHA-256 hash.
    """

    return sha256(file).lower() == expected_hash.lower()


# ---------------------------------------------------------


def hash_string(text: str) -> str:
    """
    SHA-256 of a string.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# ---------------------------------------------------------


def hash_bytes(data: bytes) -> str:
    """
    SHA-256 of bytes.
    """

    return hashlib.sha256(data).hexdigest()