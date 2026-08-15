from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    reader = PdfReader(str(path))

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text).strip()


def load_docx(file_path: str) -> str:
    """Extract text from a DOCX resume."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = Document(str(path))

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text.strip())

    return "\n".join(text).strip()


def load_resume(file_path: str) -> str:
    """Load a PDF or DOCX resume."""

    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        return load_pdf(file_path)

    if path.suffix.lower() == ".docx":
        return load_docx(file_path)

    raise ValueError(
        "Unsupported file type. Please upload a PDF or DOCX resume."
    )

