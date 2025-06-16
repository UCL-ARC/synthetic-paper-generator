# Synthetic Scientific Paper Generator

This tool generates LaTeX documents using PyLaTeX with configurable structures, renders them as PDFs, and saves the original structure in JSON format for OCR comparison.

## Quick Start

###  System Requirements

- Python 3.11 or higher
- Tesseract OCR (for OCR capabilities)
- Poppler (for PDF processing)

### Installing System Dependencies

On macOS:
```bash
brew install tesseract poppler
```

On Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the generator:
```bash
python src/synthetic_paper_generator/generate.py
```

3. Run OCR pipeline:
```bash
python src/synthetic_paper_generator/ocr_pipeline.py
```

## Output Structure

The tool generates the following directory structure under the `output` folder:

```
output/
├── pdf/                    # Generated PDF files
│   └── paper_*.pdf        # Generated scientific papers
├── json/                   # Original structure in JSON format
│   └── paper_*.json       # JSON files containing paper structure
└── ocr_txt/               # OCR results from different engines
    ├── tesseract/         # Tesseract OCR results
    │   └── paper_*.txt
    ├── marker/            # Marker PDF parser results
    │   └── paper_*.txt
    └── docling/           # Docling OCR results
        └── paper_*.txt
```

### Understanding the Output

1. **PDF Files** (`output/pdf/`):
   - Generated scientific papers in PDF format
   - Each file is named `paper_<timestamp>.pdf`

2. **JSON Structure** (`output/json/`):
   - Contains the original structure of each generated paper
   - Useful for comparing OCR results with ground truth
   - Each file corresponds to a PDF file with the same name

3. **OCR Results** (`output/ocr_txt/`):
   - Results from different OCR engines
   - Each engine has its own subdirectory
   - Text files contain extracted content from PDFs
   - Useful for comparing OCR accuracy across different engines

## Configuration

You can customize the document generation by modifying `config.yaml`. The configuration file allows you to:
- Adjust document structure
- Modify content generation parameters
- Change output formats and locations


## About

### Project Team

Sagar Uprety ([s.uprety@ucl.ac.uk](mailto:s.uprety@ucl.ac.uk))
Tim Repke ([tim.repke@pik-potsdam.de](mailto:tim.repke@pik-potsdam.de))
<!-- TODO: how do we have an array of collaborators ? -->



### Building Documentation

The MkDocs HTML documentation can be built locally by running

```sh
tox -e docs
```

from the root of the repository. The built documentation will be written to
`site`.

Alternatively to build and preview the documentation locally, in a Python
environment with the optional `docs` dependencies installed, run

```sh
mkdocs serve
```

## Roadmap

- [x] Initial Research
- [ ] Minimum viable product <-- You are Here
- [ ] Alpha Release
- [ ] Feature-Complete Release
