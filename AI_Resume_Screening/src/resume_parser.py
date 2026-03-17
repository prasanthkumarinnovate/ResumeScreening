import logging
from pdfminer.high_level import extract_text
import docx

# hide unnecessary pdfminer warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_text_from_pdf(file_path):
    text = extract_text(file_path)
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return " ".join(text)


def parse_resume(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format")