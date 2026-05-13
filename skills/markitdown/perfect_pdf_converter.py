#!/usr/bin/env python3
"""
Perfect PDF Converter - Combines MarkItDown text extraction with PyMuPDF image extraction.

Usage:
    python perfect_pdf_converter.py document.pdf
    python perfect_pdf_converter.py document.pdf --output-dir ./output
"""

import fitz  # PyMuPDF
from markitdown import MarkItDown
from pathlib import Path
import re
import argparse
from typing import Tuple, List, Optional


class PerfectPDFConverter:
    """
    Convert PDFs to Markdown with both text and images.
    Combines MarkItDown's text extraction with PyMuPDF's image extraction.
    """

    def __init__(self, output_dir: str = "output", insert_strategy: str = "smart"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.insert_strategy = insert_strategy
        self.markitdown = MarkItDown()

    def convert(self, pdf_path: str) -> Tuple[str, List[str]]:
        """
        Convert PDF to markdown with images.

        Returns:
            (markdown_path, list_of_image_paths)
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        stem = pdf_path.stem
        images_dir = self.output_dir / f"{stem}_images"
        images_dir.mkdir(exist_ok=True)

        # Step 1: Extract text with MarkItDown
        print(f"Extracting text with MarkItDown...")
        result = self.markitdown.convert(str(pdf_path))
        markdown_lines = result.markdown.split('\n')

        # Step 2: Extract images with PyMuPDF
        print(f"Extracting images with PyMuPDF...")
        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)
        image_files = []

        for page_num, page in enumerate(doc, start=1):
            print(f"  Processing page {page_num}/{total_pages}...")
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Save image
                image_filename = images_dir / f"page{page_num}_fig{img_index}.{image_ext}"
                with open(image_filename, "wb") as f:
                    f.write(image_bytes)

                image_files.append(str(image_filename))

                # Find insertion point in markdown
                self._insert_image_reference(markdown_lines, page_num, img_index, image_filename, total_pages)

        doc.close()

        # Step 3: Clean up markdown
        markdown_lines = self._clean_markdown(markdown_lines)

        # Step 4: Write final markdown
        output_path = self.output_dir / f"{stem}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(markdown_lines))

        print(f"\nConversion complete!")
        print(f"  Markdown: {output_path}")
        print(f"  Images: {len(image_files)} in {images_dir}")

        return str(output_path), image_files

    def _insert_image_reference(self, lines: List[str], page_num: int, fig_num: int,
                                 image_path: Path, total_pages: int):
        """Insert image reference at appropriate position."""
        relative_path = image_path.relative_to(self.output_dir.parent)
        image_ref = f"\n\n![Figure {page_num}-{fig_num}]({relative_path})\n\n"

        if self.insert_strategy == "smart":
            self._smart_insert(lines, page_num, fig_num, total_pages, image_ref)
        else:
            self._linear_insert(lines, page_num, total_pages, image_ref)

    def _smart_insert(self, lines: List[str], page_num: int, fig_num: int,
                       total_pages: int, image_ref: str):
        """Try to find appropriate position using page markers."""
        # Page marker patterns
        page_patterns = [
            (rf"Page\s+{page_num}\s", 0),      # "Page 1", "Page 2"
            (rf"Page\s+{page_num}$", 0),      # "Page 1" at end
            (rf"第\s*{page_num}\s*页", 0),     # Chinese page marker
            (rf"^#{1,3}\s*{page_num}\s", 0),  # Markdown heading with number
            (rf"^\s*{page_num}\s", 10),       # Just the number
        ]

        insert_idx = -1

        # Search for page markers
        for pattern, offset in page_patterns:
            for i, line in enumerate(lines):
                if re.search(pattern, line, re.IGNORECASE | re.MULTILINE):
                    insert_idx = min(len(lines), i + offset + 1)
                    break
            if insert_idx >= 0:
                break

        # If no page marker found, estimate position
        if insert_idx < 0:
            lines_per_page = max(30, len(lines) // max(1, total_pages))
            insert_idx = min(len(lines), page_num * lines_per_page)

        # Insert image reference
        lines.insert(insert_idx, image_ref)

    def _linear_insert(self, lines: List[str], page_num: int, total_pages: int, image_ref: str):
        """Insert images linearly throughout the document."""
        lines_per_page = max(30, len(lines) // max(1, total_pages))
        insert_idx = min(len(lines), page_num * lines_per_page)
        lines.insert(insert_idx, image_ref)

    def _clean_markdown(self, lines: List[str]) -> List[str]:
        """Clean up markdown formatting."""
        # Remove excessive empty lines
        cleaned = []
        prev_empty = False

        for line in lines:
            is_empty = not line.strip()

            if is_empty:
                if not prev_empty:
                    cleaned.append("")
                prev_empty = True
            else:
                cleaned.append(line)
                prev_empty = False

        return cleaned


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown with text and images"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-o", "--output-dir", default="output",
                        help="Output directory (default: output)")
    parser.add_argument("-s", "--strategy", choices=["smart", "linear"],
                        default="smart", help="Image insertion strategy")

    args = parser.parse_args()

    converter = PerfectPDFConverter(
        output_dir=args.output_dir,
        insert_strategy=args.strategy
    )

    try:
        md_path, images = converter.convert(args.pdf)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
