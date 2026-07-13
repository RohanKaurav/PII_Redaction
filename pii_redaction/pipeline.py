from typing import List
from .types import PIIMatch
from .detect import detect_regex, detect_ner
from .resolve import resolve_overlaps
from .map import FakeMapper

def run_all_detectors(text: str, page: int, nlp) -> List[PIIMatch]:
    matches = detect_regex(text, page)
    matches += detect_ner(text, page, nlp)
    return resolve_overlaps(matches)

def redact_page_text(text: str, matches: List[PIIMatch], mapper: FakeMapper) -> str:
    for m in sorted(matches, key=lambda m: m.start, reverse=True):
        fake = mapper.get_fake(m.text, m.pii_type)
        text = text[: m.start] + fake + text[m.end :]
    return text
