import io
import re
from pathlib import Path

import chardet
import docx
import fitz
import markdown2
from bs4 import BeautifulSoup

SUPPORTED_EXTENSIONS = {"pdf", "docx", "html", "htm", "md", "srt", "txt", "text"}


def extension_from_filename(filename: str) -> str:
    return Path(filename or "").suffix.lower().lstrip(".")


def _decode_text(content: bytes) -> str:
    detected = chardet.detect(content)
    encoding = detected.get("encoding") or "utf-8"
    return content.decode(encoding, errors="ignore")


def extract_text_from_bytes(content: bytes, filename: str) -> str:
    file_type = extension_from_filename(filename)
    if file_type not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type '.{file_type}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
    if file_type == "pdf":
        with fitz.open(stream=content, filetype="pdf") as pdf:
            return "\n".join(page.get_text() for page in pdf)
    if file_type == "docx":
        document = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in document.paragraphs)
    text = _decode_text(content)
    if file_type in ("html", "htm"):
        return BeautifulSoup(text, "html.parser").get_text("\n")
    if file_type == "md":
        html = markdown2.markdown(text)
        return BeautifulSoup(html, "html.parser").get_text("\n")
    if file_type == "srt":
        text = re.sub(r"(?m)^\s*\d+\s*\n", "", text)
        text = re.sub(r"(?m)^\s*\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}.*\n?", "", text)
        return text
    return text
