from pathlib import Path
from pypdf import PdfReader, PdfWriter


class PDFService:

    @staticmethod
    def split(pdf_path: Path, start: int, end: int, output_path: Path):
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as f:
            writer.write(f)

    @staticmethod
    def merge(pdf_paths: list[Path], output_path: Path):
        writer = PdfWriter()

        for path in pdf_paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

    @staticmethod
    def delete_pages(pdf_path: Path, pages_to_delete: set[int], output_path: Path):
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages, start=1):
            if i not in pages_to_delete:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

    @staticmethod
    def reorder(pdf_path: Path, new_order: list[int], output_path: Path):
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page_num in new_order:
            writer.add_page(reader.pages[page_num - 1])

        with open(output_path, "wb") as f:
            writer.write(f)
