import os
from pathlib import Path
from typing import List, Optional
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from docling.document_converter import DocumentConverter


def run_tesseract_ocr(pdf_path: Path, output_txt_path: Path) -> None:
    """Run OCR on a PDF using Tesseract OCR engine.

    Args:
        pdf_path: Path to the input PDF file
        output_txt_path: Path where the OCR text output will be saved
    """
    # Convert PDF to images
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""
    for page_num, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text += f"\n--- PAGE {page_num+1} ---\n"
        full_text += text

    with open(output_txt_path, 'w') as f:
        f.write(full_text)


def run_marker_ocr(pdf_path: Path, output_txt_path: Path) -> None:
    """Run OCR on a PDF using Marker PDF parser.

    Args:
        pdf_path: Path to the input PDF file
        output_txt_path: Path where the OCR text output will be saved
    """
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )
    rendered = converter(str(pdf_path))
    text, _, _ = text_from_rendered(rendered)
    with open(output_txt_path, 'w') as f:
        f.write(text)


def run_docling_ocr(pdf_path: Path, output_txt_path: Path) -> None:
    """Run OCR on a PDF using Docling.

    Args:
        pdf_path: Path to the input PDF file
        output_txt_path: Path where the OCR text output will be saved
    """
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    markdown_output = result.document.export_to_markdown()
    with open(output_txt_path, 'w') as f:
        f.write(markdown_output)


def run_ocr_on_pdf(
    pdf_path: Path,
    output_txt_path: Path,
    ocr_library: str = "tesseract"
) -> None:
    """Run OCR on a PDF using the specified OCR library.

    Args:
        pdf_path: Path to the input PDF file
        output_txt_path: Path where the OCR text output will be saved
        ocr_library: Name of the OCR library to use (default: "tesseract")
    """
    if ocr_library == "tesseract":
        run_tesseract_ocr(pdf_path, output_txt_path)
    elif ocr_library == "marker":
        run_marker_ocr(pdf_path, output_txt_path)
    elif ocr_library == "docling":
        run_docling_ocr(pdf_path, output_txt_path)
    else:
        raise ValueError(f"Unsupported OCR library: {ocr_library}")


def process_pdf_directory(
    pdf_dir: Path,
    output_base_dir: Path,
    ocr_library: str = "tesseract"
) -> None:
    """Process all PDFs in a directory using the specified OCR library.

    Args:
        pdf_dir: Directory containing PDF files
        output_base_dir: Base directory for OCR output
        ocr_library: Name of the OCR library to use (default: "tesseract")
    """
    # Create library-specific output directory
    output_dir = output_base_dir / ocr_library
    os.makedirs(output_dir, exist_ok=True)

    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith('.pdf'):
            pdf_path = pdf_dir / pdf_file
            output_txt_path = output_dir / pdf_file.replace('.pdf', '.txt')
            print(f"Running {ocr_library} OCR on {pdf_file}")
            run_ocr_on_pdf(pdf_path, output_txt_path, ocr_library)


if __name__ == "__main__":
    # Get the project root directory (2 levels up from this file)
    project_root = Path(__file__).parent.parent.parent
    pdf_dir = project_root / 'output' / 'pdf'
    output_base_dir = project_root / 'output' / 'ocr_txt'
    
    # Process PDFs with all OCR libraries
    for ocr_lib in ["tesseract", "marker", "docling"]:
        process_pdf_directory(pdf_dir, output_base_dir, ocr_lib)