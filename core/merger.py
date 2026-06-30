from __future__ import annotations

from pathlib import Path
from typing import List

import fitz  # PyMuPDF


class PDFMerger:

    def __init__(self):
        self.output_document = fitz.open()

    # ---------------------------------------------------------

    def merge(
        self,
        pdf_files: List[Path],
        output_file: Path,
        progress_callback=None,
    ):

        total = len(pdf_files)

        if total == 0:
            raise ValueError("No PDF files to merge.")

        for index, pdf in enumerate(pdf_files, start=1):

            try:

                source = fitz.open(pdf)

                # Bookmark at first page of inserted document
                start_page = self.output_document.page_count

                self.output_document.insert_pdf(source)

                toc = self.output_document.get_toc()

                toc.append(
                    [
                        1,
                        pdf.stem,
                        start_page + 1,
                    ]
                )

                self.output_document.set_toc(toc)

                source.close()

                if progress_callback:
                    progress_callback(index, total, pdf)

            except Exception as e:
                print(f"Failed to merge: {pdf}")
                print(e)

        self.output_document.save(
            output_file,
            garbage=4,
            deflate=True,
        )

        self.output_document.close()

    # ---------------------------------------------------------

    def merge_from_groups(
        self,
        duplicate_groups,
        output_file: Path,
        keep_original=True,
        progress_callback=None,
    ):

        files = []

        for group in duplicate_groups:

            if keep_original:
                files.append(group.original.path)
            else:
                files.append(group.original.path)

                for dup in group.duplicates:
                    files.append(dup.path)

        self.merge(
            files,
            output_file,
            progress_callback,
        )

    # ---------------------------------------------------------

    @staticmethod
    def merge_simple(
        pdf_files: List[Path],
        output_file: Path,
    ):

        merger = PDFMerger()

        merger.merge(
            pdf_files,
            output_file,
        )