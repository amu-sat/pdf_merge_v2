from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent

DIST = ROOT / "dist"
BUILD = ROOT / "build"

APP_NAME = "ZipPDFMerger"


# ----------------------------------------------------------


def remove_old_build():

    for folder in (DIST, BUILD):

        if folder.exists():
            shutil.rmtree(folder)

    for spec in ROOT.glob("*.spec"):
        spec.unlink()


# ----------------------------------------------------------


def find_icon():

    candidates = [
        ROOT / "resources" / "icon.ico",
        ROOT / "resources" / "images" / "icon.ico",
    ]

    for icon in candidates:
        if icon.exists():
            return icon

    return None


# ----------------------------------------------------------


def find_entry():

    candidates = [
        ROOT / "main.py",
        ROOT / "app.py",
    ]

    for entry in candidates:
        if entry.exists():
            return entry

    raise FileNotFoundError(
        "Neither main.py nor app.py found."
    )


# ----------------------------------------------------------


def build():

    command = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--clean",

        "--noconfirm",

        "--onefile",

        "--windowed",

        "--name",
        APP_NAME,
    ]

    icon = find_icon()

    if icon:

        command.extend(
            [
                "--icon",
                str(icon),
            ]
        )

    entry = find_entry()

    command.append(str(entry))

    print()
    print("=" * 60)
    print("Running:")
    print()
    print(" ".join(command))
    print("=" * 60)

    subprocess.run(command, check=True)


# ----------------------------------------------------------


def main():

    print("=" * 60)
    print("Building ZipPDFMerger")
    print("=" * 60)

    remove_old_build()

    build()

    print()
    print("=" * 60)
    print("Build Successful")
    print("=" * 60)
    print()
    print("Executable:")
    print(DIST / f"{APP_NAME}.exe")


# ----------------------------------------------------------

if __name__ == "__main__":
    main()