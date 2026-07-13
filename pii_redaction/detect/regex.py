import re
from typing import List
from pii_redaction.types import PIIMatch, PIIType

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Indian + generic phone formats
PHONE_RE = re.compile(
    r"(\+?\d{1,3}[-.\s]?)?"          # optional country code
    r"(\(?\d{2,5}\)?[-.\s]?)?"       # optional area/STD code
    r"\d{3,5}[-.\s]?\d{3,5}"         # main number, allow one internal split
    r"\b"
)
PHONE_MIN_DIGITS = 10
PHONE_MAX_DIGITS = 13

COMPANY_SUFFIX_RE = re.compile(
    r"\b(?:[A-Z][A-Za-z0-9&\'-]*[ ]+(?:(?:of|and|the|&|for)[ ]+)?){1,8}?"
    r"(?:Private[ ]+Limited|Limited|LLP|Ltd\.?|Pvt\.?[ ]*Ltd\.?|Inc\.?|Corporation|Corp\.?)\b"
)

SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CREDIT_CARD_RE = re.compile(r"\b(?:\d[ -]?){13,16}\b")
IP_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")
PAN_RE = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")

DOB_TRIGGER_RE = re.compile(
    r"(date of birth|born on|\bDOB\b)\s*[:\-]?\s*"
    r"([0-3]?\d[-/. ](?:[0-3]?\d|[A-Za-z]+)[-/. ]\d{2,4})",
    re.IGNORECASE,
)

def luhn_valid(digits: str) -> bool:
    digits_list = [int(d) for d in digits]
    checksum = 0
    parity = len(digits_list) % 2
    for i, d in enumerate(digits_list):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def detect_regex(text: str, page: int) -> List[PIIMatch]:
    matches = []

    for m in EMAIL_RE.finditer(text):
        matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.EMAIL, page, "regex"))

    for m in PHONE_RE.finditer(text):
        digit_count = len(re.sub(r"\D", "", m.group()))
        if PHONE_MIN_DIGITS <= digit_count <= PHONE_MAX_DIGITS:
            matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.PHONE, page, "regex"))

    for m in SSN_RE.finditer(text):
        matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.SSN, page, "regex"))

    for m in CREDIT_CARD_RE.finditer(text):
        raw_digits = re.sub(r"[ -]", "", m.group())
        if len(raw_digits) in (13, 14, 15, 16) and luhn_valid(raw_digits):
            matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.CREDIT_CARD, page, "regex"))

    for m in IP_RE.finditer(text):
        matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.IP_ADDRESS, page, "regex"))

    for m in PAN_RE.finditer(text):
        matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.PAN, page, "regex"))

    for m in DOB_TRIGGER_RE.finditer(text):
        date_span = m.span(2)
        matches.append(PIIMatch(date_span[0], date_span[1], m.group(2), PIIType.DOB, page, "regex"))

    for m in COMPANY_SUFFIX_RE.finditer(text):
        matches.append(PIIMatch(m.start(), m.end(), m.group(), PIIType.ORG, page, "regex"))

    return matches
