from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import hashlib

import fitz  # PyMuPDF


@dataclass
class PDFInfo:
    path: Path
    size: int
    pages: int
    sha256: str = ""


@dataclass
class DuplicateGroup:
    original: PDFInfo
    duplicates: List[PDFInfo]


class DuplicateDetector:
    """
    Detect duplicate PDFs using:
        1. File Size
        2. Page Count
        3. SHA256 Hash
    """

    def __init__(self):
        pass

    # -------------------------------------------------------

    def scan(self, pdf_files: List[Path]) -> List[DuplicateGroup]:
        """
        Returns duplicate groups.
        """

        infos = []

        for pdf in pdf_files:
            try:
                infos.append(
                    PDFInfo(
                        path=pdf,
                        size=pdf.stat().st_size,
                        pages=self._page_count(pdf),
                    )
                )
            except Exception:
                continue

        # Stage 1
        size_groups = self._group_by_size(infos)

        # Stage 2
        page_groups = self._group_by_pages(size_groups)

        # Stage 3
        duplicates = self._group_by_hash(page_groups)

        return duplicates

    # -------------------------------------------------------

    def _page_count(self, pdf: Path) -> int:
        try:
            with fitz.open(pdf) as doc:
                return doc.page_count
        except Exception:
            return -1

    # -------------------------------------------------------

    def _sha256(self, pdf: Path) -> str:

        h = hashlib.sha256()

        with open(pdf, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    # -------------------------------------------------------

    def _group_by_size(
        self,
        infos: List[PDFInfo],
    ) -> List[List[PDFInfo]]:

        groups: Dict[int, List[PDFInfo]] = defaultdict(list)

        for info in infos:
            groups[info.size].append(info)

        return [g for g in groups.values() if len(g) > 1]

    # -------------------------------------------------------

    def _group_by_pages(
        self,
        size_groups: List[List[PDFInfo]],
    ) -> List[List[PDFInfo]]:

        output = []

        for group in size_groups:

            pages: Dict[int, List[PDFInfo]] = defaultdict(list)

            for info in group:
                pages[info.pages].append(info)

            for g in pages.values():
                if len(g) > 1:
                    output.append(g)

        return output

    # -------------------------------------------------------

    def _group_by_hash(
        self,
        page_groups: List[List[PDFInfo]],
    ) -> List[DuplicateGroup]:

        duplicate_groups = []

        for group in page_groups:

            hashes: Dict[str, List[PDFInfo]] = defaultdict(list)

            for info in group:

                info.sha256 = self._sha256(info.path)

                hashes[info.sha256].append(info)

            for dup in hashes.values():

                if len(dup) < 2:
                    continue

                duplicate_groups.append(
                    DuplicateGroup(
                        original=dup[0],
                        duplicates=dup[1:],
                    )
                )

        return duplicate_groups