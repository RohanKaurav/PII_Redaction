import re
import pdfplumber
from typing import List
from .detect.regex import PHONE_MIN_DIGITS

def fix_wrapped_phone_numbers(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r"(Telephone|Tel)[:\s].*\d", line, re.IGNORECASE):
            digits_so_far = len(re.sub(r"\D", "", line.split(":")[-1]))
            if digits_so_far < PHONE_MIN_DIGITS and i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if re.fullmatch(r"\d{3,5}", nxt):
                    line = line.rstrip() + " " + nxt
                    i += 1
        out.append(line)
        i += 1
    return "\n".join(out)

def extract_pages(pdf_path: str) -> List[str]:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            text = fix_wrapped_phone_numbers(text)
            pages.append(text)
    return pages
