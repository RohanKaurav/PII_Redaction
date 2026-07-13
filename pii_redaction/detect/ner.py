import re
import spacy
from typing import List
from pii_redaction.types import PIIMatch, PIIType
from pii_redaction.config import (
    NER_LABEL_MAP,
    ORG_ALLOWLIST,
    FIELD_LABEL_ALLOWLIST,
    DEFINED_TERM_STOPLIST,
    COUNTRY_LEVEL_STOPLIST
)

def is_garbled(text: str) -> bool:
    tokens = text.split()
    if not tokens:
        return True
    short = sum(1 for t in tokens if len(t) <= 2)
    return (short / len(tokens)) > 0.4

def is_low_confidence_entity(text: str) -> bool:
    stripped = text.strip()
    if re.match(r"^(the|this|our)\s", stripped, re.IGNORECASE):
        return True
    if "/" in stripped or "(" in stripped or ")" in stripped:
        return True
    return False

def load_ner_model():
    return spacy.load("en_core_web_sm")

def _ner_pass(text: str, page: int, nlp, source_label: str, original_text: str) -> List[PIIMatch]:
    matches = []
    doc = nlp(text)
    for ent in doc.ents:
        pii_type = NER_LABEL_MAP.get(ent.label_)
        if pii_type is None:
            continue

        raw = ent.text.strip()
        normalized = re.sub(r"\s+", " ", raw).lower()

        if len(raw) < 2:
            continue
        if pii_type == PIIType.ORG and normalized in ORG_ALLOWLIST:
            continue
        if normalized in FIELD_LABEL_ALLOWLIST:
            continue
        if normalized in DEFINED_TERM_STOPLIST:
            continue
        if pii_type == PIIType.ADDRESS and normalized in COUNTRY_LEVEL_STOPLIST:
            continue
        if is_garbled(raw):
            continue
        if is_low_confidence_entity(raw):
            continue

        true_text = original_text[ent.start_char:ent.end_char]
        matches.append(PIIMatch(ent.start_char, ent.end_char, true_text, pii_type, page, source_label))
    return matches

def detect_ner(text: str, page: int, nlp) -> List[PIIMatch]:
    original_matches = _ner_pass(text, page, nlp, "ner", original_text=text)
    titled_matches = _ner_pass(text.title(), page, nlp, "ner_titlecased", original_text=text)
    return original_matches + titled_matches
