from __future__ import annotations

from pathlib import Path
from typing import List

import fitz  # PyMuPDF


class BookmarkManager:
    """
    Handles bookmark (Table of Contents) creation for merged PDFs.
    """

    def __init__(self):
        self.toc = []

    # ---------------------------------------------------------

    def clear(self):
        self.toc.clear()

    # ---------------------------------------------------------

    def add(
        self,
        title: str,
        page_number: int,
        level: int = 1,
    ):
        """
        Add a bookmark.

        Parameters
        ----------
        title : Bookmark title
        page_number : 1-based page number
        level : Bookmark level (1=root)
        """

        self.toc.append(
            [
                level,
                title,
                page_number,
            ]
        )

    # ---------------------------------------------------------

    def add_pdf(
        self,
        pdf: Path,
        start_page: int,
        level: int = 1,
    ):
        """
        Create bookmark using filename.
        """

        self.add(
            title=pdf.stem,
            page_number=start_page + 1,
            level=level,
        )

    # ---------------------------------------------------------

    def apply(
        self,
        document: fitz.Document,
    ):
        """
        Apply bookmarks to merged document.
        """

        if self.toc:
            document.set_toc(self.toc)

    # ---------------------------------------------------------

    def export(self):

        return self.toc.copy()

    # ---------------------------------------------------------

    def import_toc(
        self,
        toc: List[list],
    ):

        self.toc = toc.copy()

    # ---------------------------------------------------------

    def build_from_documents(
        self,
        pdf_files: List[Path],
    ):

        """
        Automatically create one bookmark per merged PDF.
        """

        self.clear()

        page = 1

        for pdf in pdf_files:

            try:

                with fitz.open(pdf) as doc:

                    self.add(
                        pdf.stem,
                        page,
                        1,
                    )

                    page += doc.page_count

            except Exception:
                continue

    # ---------------------------------------------------------

    def merge_existing_bookmarks(
        self,
        merged_doc: fitz.Document,
        pdf_files: List[Path],
    ):
        """
        Copies existing bookmarks from source PDFs while
        maintaining correct page offsets.
        """

        self.clear()

        offset = 0

        for pdf in pdf_files:

            try:

                with fitz.open(pdf) as doc:

                    toc = doc.get_toc()

                    if toc:

                        for level, title, page in toc:

                            self.toc.append(
                                [
                                    level,
                                    title,
                                    page + offset,
                                ]
                            )

                    else:

                        self.toc.append(
                            [
                                1,
                                pdf.stem,
                                offset + 1,
                            ]
                        )

                    offset += doc.page_count

            except Exception:

                continue

        merged_doc.set_toc(self.toc)