from __future__ import annotations

from pathlib import Path
from typing import List

import fitz  # PyMuPDF


# ---------------------------------------------------------


def page_count(pdf: Path) -> int:
    """
    Return number of pages in a PDF.
    """

    try:
        with fitz.open(pdf) as doc:
            return doc.page_count
    except Exception:
        return 0


# ---------------------------------------------------------


def is_valid_pdf(pdf: Path) -> bool:
    """
    Check whether a PDF can be opened.
    """

    try:
        with fitz.open(pdf):
            return True
    except Exception:
        return False


# ---------------------------------------------------------


def metadata(pdf: Path) -> dict:
    """
    Return PDF metadata.
    """

    try:
        with fitz.open(pdf) as doc:
            return doc.metadata
    except Exception:
        return {}


# ---------------------------------------------------------


def title(pdf: Path) -> str:

    data = metadata(pdf)

    return data.get("title") or pdf.stem


# ---------------------------------------------------------


def dimensions(pdf: Path) -> tuple[float, float]:

    try:
        with fitz.open(pdf) as doc:

            if doc.page_count == 0:
                return (0.0, 0.0)

            page = doc.load_page(0)
            rect = page.rect

            return rect.width, rect.height

    except Exception:
        return (0.0, 0.0)


# ---------------------------------------------------------


def bookmarks(pdf: Path) -> list:

    try:
        with fitz.open(pdf) as doc:
            return doc.get_toc()
    except Exception:
        return []


# ---------------------------------------------------------


def encrypted(pdf: Path) -> bool:

    try:
        with fitz.open(pdf) as doc:
            return doc.is_encrypted
    except Exception:
        return False


# ---------------------------------------------------------


def merge(
    pdf_files: List[Path],
    output: Path,
):

    merged = fitz.open()

    try:

        for pdf in pdf_files:

            with fitz.open(pdf) as src:
                merged.insert_pdf(src)

        merged.save(
            output,
            garbage=4,
            deflate=True,
        )

    finally:
        merged.close()


# ---------------------------------------------------------


def extract_pages(
    source: Path,
    pages: List[int],
    output: Path,
):

    src = fitz.open(source)
    dst = fitz.open()

    try:

        for page in pages:

            if 0 <= page < src.page_count:
                dst.insert_pdf(
                    src,
                    from_page=page,
                    to_page=page,
                )

        dst.save(output)

    finally:
        src.close()
        dst.close()


# ---------------------------------------------------------


def split(
    source: Path,
    output_dir: Path,
):

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with fitz.open(source) as src:

        for page_no in range(src.page_count):

            dst = fitz.open()

            dst.insert_pdf(
                src,
                from_page=page_no,
                to_page=page_no,
            )

            outfile = (
                output_dir
                / f"{source.stem}_{page_no + 1}.pdf"
            )

            dst.save(outfile)
            dst.close()


# ---------------------------------------------------------


def rotate(
    source: Path,
    output: Path,
    angle: int,
):

    with fitz.open(source) as doc:

        for page in doc:
            page.set_rotation(angle)

        doc.save(output)


# ---------------------------------------------------------


def compress(
    source: Path,
    output: Path,
):

    with fitz.open(source) as doc:

        doc.save(
            output,
            garbage=4,
            clean=True,
            deflate=True,
        )


# ---------------------------------------------------------


def file_info(pdf: Path) -> dict:

    return {
        "name": pdf.name,
        "path": str(pdf),
        "pages": page_count(pdf),
        "size": pdf.stat().st_size if pdf.exists() else 0,
        "encrypted": encrypted(pdf),
        "metadata": metadata(pdf),
    }