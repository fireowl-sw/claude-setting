# MarkItDown Document Converter

Microsoft's MarkItDown is a lightweight Python utility for converting various document formats to Markdown, optimized for LLM consumption.

## Quick Start: PDF to Markdown with Images

```bash
# Use the built-in script
python ~/.claude/skills/markitdown/perfect_pdf_converter.py document.pdf

# Or install and use the simple function below
pip install PyMuPDF pdfplumber
```

Then in Python:
```python
# See "Simple One-Script Solution" section below for the function
pdf_to_markdown_with_images("document.pdf")
```

## Installation

```bash
pip install 'markitdown[all]'
```

Or install specific format dependencies:

```bash
pip install 'markitdown[pdf,docx,pptx]'
```

## Supported Formats

- **Documents**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **Images**: EXIF metadata + OCR, LLM-powered descriptions
- **Audio**: EXIF metadata + speech transcription (WAV, MP3)
- **Web**: HTML, Wikipedia, YouTube transcripts, RSS feeds
- **Text**: CSV, JSON, XML, Jupyter Notebooks (IPYNB)
- **Other**: ZIP files (iterates contents), EPUB, Outlook MSG

## Python API

### Basic Usage

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("document.pdf")
print(result.markdown)     # Converted markdown content
print(result.title)         # Optional extracted title
```

### Stream Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()

# From file path
result = md.convert_local("data.xlsx")

# From URL
result = md.convert_uri("https://example.com/document.pdf")

# From binary stream
with open("file.docx", "rb") as f:
    result = md.convert_stream(f)

# From requests Response
import requests
response = requests.get("https://example.com/doc.pdf")
result = md.convert_response(response)
```

### LLM-Powered Image Descriptions

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe this image in detail"
)

result = md.convert("chart.png")
print(result.markdown)  # Includes LLM-generated description
```

### Azure Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="https://<resource>.cognitiveservices.azure.com",
    docintel_credential="<api-key>",
    docintel_file_types=["pdf", "jpg", "png"]
)

result = md.convert("scanned.pdf")
```

## Command-Line

```bash
# Basic conversion
markitdown document.pdf > output.md

# Specify output file
markitdown document.pdf -o output.md

# Pipe content
cat document.docx | markitdown > output.md

# Use Azure Document Intelligence
markitdown doc.pdf -o output.md -d -e "<endpoint>"

# Enable plugins
markitdown --use-plugins document.pdf
```

## Custom Converters

```python
from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult
from markitdown import StreamInfo

class CustomConverter(DocumentConverter):
    def accepts(self, file_stream, stream_info, **kwargs):
        # Return True if this converter handles the file
        return stream_info.extension == ".custom"

    def convert(self, file_stream, stream_info, **kwargs):
        # Convert the file content to markdown
        content = file_stream.read().decode("utf-8")
        return DocumentConverterResult(
            markdown=f"# Custom Document\n\n{content}",
            title="Custom Title"
        )

# Register the custom converter
md = MarkItDown()
md.register_converter(CustomConverter())
result = md.convert("file.custom")
```

## Error Handling

```python
from markitdown import (
    MarkItDown,
    UnsupportedFormatException,
    FileConversionException,
    MissingDependencyException
)

md = MarkItDown()

try:
    result = md.convert("document.pdf")
except UnsupportedFormatException:
    print("File type not supported")
except FileConversionException as e:
    print(f"Conversion failed: {e.attempts}")
except MissingDependencyException as e:
    print(f"Missing dependency: {e}")
```

## Key Classes

- `MarkItDown`: Main converter class
- `DocumentConverterResult`: Contains `markdown` and `title`
- `DocumentConverter`: Base class for custom converters
- `StreamInfo`: Metadata about the file (mimetype, extension, charset, url)

## Best Practices

1. **Use `[all]` for development** - Install all optional dependencies
2. **Stream large files** - Use `convert_stream()` for memory efficiency
3. **Handle exceptions** - Catch specific exceptions for better error messages
4. **Leverage LLM for images** - Enable image descriptions for PPTX/images
5. **Batch processing** - Reuse `MarkItDown` instance for multiple files

---

## PDF Conversion Limitations

### MarkItDown PDF Limitations

| Feature | MarkItDown Standard | MarkItDown + Azure |
|---------|-------------------|-------------------|
| Text extraction | ✅ | ✅ |
| Image extraction | ❌ | ⚠️ Limited (OCR only) |
| Save original images | ❌ | ❌ |
| Tables | ⚠️ Plain text | ✅ Structured |
| OCR | ❌ | ✅ High-res |

**Important**: MarkItDown is designed for LLM text consumption, NOT for preserving document visual fidelity.

---

## Enhanced PDF Conversion (Text + Images)

For PDFs with images, use these alternative tools:

### 1. PyMuPDF (fitz) - Recommended

```bash
pip install PyMuPDF
```

```python
import fitz  # PyMuPDF
from pathlib import Path

def pdf_to_markdown_with_images(pdf_path: str, output_dir: str = "output"):
    """Convert PDF to Markdown with extracted images."""
    doc = fitz.open(pdf_path)
    Path(output_dir).mkdir(exist_ok=True)

    markdown_content = []
    image_counter = 0

    for page_num, page in enumerate(doc, start=1):
        # Extract text
        text = page.get_text()
        if text.strip():
            markdown_content.append(f"\n## Page {page_num}\n\n{text}")

        # Extract images
        image_list = page.get_images()
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_dir}/page{page_num}_img{img_index}.{image_ext}"

            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)

            markdown_content.append(f"\n![Figure {page_num}-{img_index}]({image_filename})\n")
            image_counter += 1

    doc.close()

    markdown_path = f"{output_dir}/content.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))

    return markdown_path, image_counter

# Usage
pdf_to_markdown_with_images("document.pdf", "output")
```

### 2. Marker - OCR + Images

```bash
pip install marker-pdf
```

```bash
# CLI
marker-pdf convert document.pdf -o output.md --extract-images

# Python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

models = load_all_models()
text, images, out_meta = convert_single_pdf("document.pdf", models)
```

### 3. Pandoc - Universal Converter

```bash
# Install
brew install pandoc  # macOS
sudo apt install pandoc  # Linux

# Convert with image extraction
pandoc document.pdf -f pdf -t markdown -o output.md --extract-media=./images
```

### 4. pdfimages (Poppler) - Raw Image Extraction

```bash
# Install
brew install poppler  # macOS
sudo apt install poppler-utils  # Linux

# Extract all images
pdfimages -all document.pdf images/image_

# List images without extracting
pdfimages -list document.pdf
```

---

## Perfect PDF Converter (Combined Approach)

### Simple One-Script Solution

```python
import fitz  # PyMuPDF
import pdfplumber
import re
from pathlib import Path

def pdf_to_markdown_with_images(pdf_path: str, output_md: str = None):
    """
    Convert PDF to Markdown with images extracted.
    Creates an 'images/' folder and saves markdown with image references.

    Args:
        pdf_path: Path to input PDF file
        output_md: Path to output markdown file (default: same name as PDF)

    Returns:
        tuple: (markdown_path, image_count)
    """
    pdf_path = Path(pdf_path)
    if output_md is None:
        output_md = pdf_path.with_suffix('.md')
    else:
        output_md = Path(output_md)

    # Create images directory
    images_dir = pdf_path.parent / "images"
    images_dir.mkdir(exist_ok=True)

    # Step 1: Extract text with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        content = []
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                content.append(f"\n\n---\n\n# Page {i}\n\n{text}")

    markdown_content = "".join(content)

    # Step 2: Extract images with PyMuPDF and map to pages
    doc = fitz.open(pdf_path)
    page_images = {}  # {page_num: [img1, img2, ...]}

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()

        if image_list:
            page_images[page_num + 1] = []
            for img_index, img in enumerate(image_list, 1):
                xref = img[0]
                base_image = doc.extract_image(xref)

                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"page{page_num + 1}_img{img_index}.{image_ext}"
                    image_path = images_dir / image_filename

                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    page_images[page_num + 1].append(image_filename)

    doc.close()

    # Step 3: Insert image references into markdown
    parts = re.split(r'(---\n\n# Page (\d+)\n\n)', markdown_content)
    new_content = []

    for i, part in enumerate(parts):
        new_content.append(part)

        # Check if this is a page content section (after page marker)
        page_match = re.search(r'# Page (\d+)', part)
        if page_match:
            page_num = int(page_match.group(1))
            # Add images at the start of next content section
            if page_num in page_images and i + 1 < len(parts):
                for img in page_images[page_num]:
                    new_content.append(f'\n![{img}](images/{img})\n')

    # Step 4: Write final markdown
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("".join(new_content))

    total_images = sum(len(imgs) for imgs in page_images.values())
    return str(output_md), total_images


# Usage
pdf_to_markdown_with_images("document.pdf")
# Or specify output:
# pdf_to_markdown_with_images("input.pdf", "output.md")
```

### Installation

```bash
pip install PyMuPDF pdfplumber
```

### Quick CLI Script

Save as `pdf2md.py`:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# ... (paste the pdf_to_markdown_with_images function above) ...

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf2md.py <input.pdf> [output.md]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_md = sys.argv[2] if len(sys.argv) > 2 else None

    md_path, img_count = pdf_to_markdown_with_images(input_pdf, output_md)
    print(f"✓ Converted: {md_path}")
    print(f"✓ Images extracted: {img_count}")
```

Usage:
```bash
python pdf2md.py document.pdf
python pdf2md.py document.pdf output.md
```

### Installation for Perfect Converter

```bash
# Core dependencies
pip install 'markitdown[all]' PyMuPDF

# Optional: system dependency for better PDF handling
brew install poppler  # macOS
```

---

## Tool Comparison Matrix

| Tool | Text | Images | Tables | OCR | Speed | Cost |
|------|------|--------|--------|-----|-------|------|
| MarkItDown | ⭐⭐⭐ | ❌ | ⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ | Free |
| MarkItDown+Azure | ⭐⭐⭐⭐ | ⚠️ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | $$$ |
| PyMuPDF | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ❌ | ⭐⭐⭐⭐ | Free |
| Marker | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | Free |
| Pandoc | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ | ⭐⭐⭐⭐ | Free |

## Recommended Workflows

```python
# Simple text-only: MarkItDown
from markitdown import MarkItDown
MarkItDown().convert("doc.pdf")

# Text + images: Use built-in script or pdf_to_markdown_with_images()
# Option 1: Built-in script
python ~/.claude/skills/markitdown/perfect_pdf_converter.py doc.pdf

# Option 2: Custom function (see "Simple One-Script Solution" section)
pdf_to_markdown_with_images("doc.pdf")

# Scanned PDF + OCR: Marker or MarkItDown+Azure
from marker.convert import convert_single_pdf
# Or use MarkItDown with docintel_endpoint
```

---

## Quick Command Reference

```bash
# MarkItDown (text only)
markitdown doc.pdf -o output.md

# Built-in script (text + images) - RECOMMENDED
python ~/.claude/skills/markitdown/perfect_pdf_converter.py doc.pdf

# Pandoc (text + images)
pandoc doc.pdf -o output.md --extract-media=images/

# pdfimages (images only)
pdfimages -all doc.pdf images/img
```
