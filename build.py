from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

ICON = PROJECT_ROOT / "resources" / "icon.ico"

APP_NAME = "PDFMerger"

MAIN_FILE = PROJECT_ROOT / "main.py"


def remove_old_build():

    for folder in (DIST_DIR, BUILD_DIR):

        if folder.exists():
            shutil.rmtree(folder)

    spec = PROJECT_ROOT / f"{APP_NAME}.spec"

    if spec.exists():
        spec.unlink()


def build():

    command = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--noconfirm",
        "--clean",

        "--windowed",

        "--onefile",

        "--name",
        APP_NAME,

        "--icon",
        str(ICON),

        "--add-data",
        "resources;resources",

        str(MAIN_FILE),
    ]

    subprocess.run(command, check=True)


def main():

    print("=" * 60)
    print("Building PDF Merger")
    print("=" * 60)

    remove_old_build()

    build()

    print()
    print("=" * 60)
    print("Build Successful")
    print("=" * 60)
    print()
    print("Executable:")
    print(DIST_DIR / f"{APP_NAME}.exe")


if __name__ == "__main__":
    main()