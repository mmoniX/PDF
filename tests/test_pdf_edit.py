"""Unit tests for PDFService edit operations."""

from pathlib import Path

import fitz

from services.pdf_edit import PDFService


def write_pdf(path: Path, page_sizes: list[tuple[float, float]]):
    """Write a PDF whose pages have the given (width, height) sizes."""
    doc = fitz.open()
    for width, height in page_sizes:
        doc.new_page(width=width, height=height)
    doc.save(path)
    doc.close()


def read_sizes(path: Path) -> list[tuple[float, float]]:
    """Return the (width, height) of every page in the PDF."""
    doc = fitz.open(path)
    sizes = [(round(page.rect.width), round(page.rect.height)) for page in doc]
    doc.close()
    return sizes


def test_split(tmp_path):
    src = tmp_path / "src.pdf"
    sizes = [(200 + i, 200 + i) for i in range(5)]
    write_pdf(src, sizes)

    out = tmp_path / "out.pdf"
    PDFService.split(src, 2, 4, out)

    assert read_sizes(out) == sizes[1:4]


def test_merge(tmp_path):
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.pdf"
    write_pdf(a, [(200, 200), (210, 210)])
    write_pdf(b, [(220, 220), (230, 230), (240, 240)])

    out = tmp_path / "out.pdf"
    PDFService.merge([a, b], out)

    assert len(read_sizes(out)) == 5


def test_delete_pages(tmp_path):
    src = tmp_path / "src.pdf"
    sizes = [(200 + i, 200 + i) for i in range(5)]
    write_pdf(src, sizes)

    out = tmp_path / "out.pdf"
    PDFService.delete_pages(src, {2, 4}, out)

    assert read_sizes(out) == [sizes[0], sizes[2], sizes[4]]


def test_reorder(tmp_path):
    src = tmp_path / "src.pdf"
    sizes = [(200, 200), (210, 210), (220, 220)]
    write_pdf(src, sizes)

    out = tmp_path / "out.pdf"
    PDFService.reorder(src, [3, 1, 2], out)

    assert read_sizes(out) == [sizes[2], sizes[0], sizes[1]]
