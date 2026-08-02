"""PDF manipulation operations, all page indices 1-based inclusive."""

from pathlib import Path

import fitz


class PDFService:
    """Stateless PDF edit operations; call methods on the class directly."""

    @staticmethod
    def split(pdf_path: Path, start: int, end: int, output_path: Path):
        """Write pages start..end (inclusive) of pdf_path into output_path."""
        with fitz.open() as out, fitz.open(pdf_path) as src:
            out.insert_pdf(src, from_page=start - 1, to_page=end - 1)
            out.save(output_path)

    @staticmethod
    def merge(pdf_paths: list[Path], output_path: Path):
        """Concatenate the given PDFs, in order, into output_path."""
        with fitz.open() as out:
            for path in pdf_paths:
                with fitz.open(path) as src:
                    out.insert_pdf(src)
            out.save(output_path)

    @staticmethod
    def delete_pages(pdf_path: Path, pages_to_delete: set[int], output_path: Path):
        """Write pdf_path without the given 1-based pages into output_path."""
        with fitz.open(pdf_path) as doc:
            doc.delete_pages(p - 1 for p in sorted(pages_to_delete))
            doc.save(output_path)

    @staticmethod
    def reorder(pdf_path: Path, new_order: list[int], output_path: Path):
        """Write pdf_path's pages in the given 1-based order into output_path."""
        with fitz.open() as out, fitz.open(pdf_path) as src:
            for page_num in new_order:
                out.insert_pdf(src, from_page=page_num - 1, to_page=page_num - 1)
            out.save(output_path)
