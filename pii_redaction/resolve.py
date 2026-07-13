from typing import List
from .types import PIIMatch, PIIType

TYPE_PRIORITY = {
    PIIType.SSN: 0,
    PIIType.CREDIT_CARD: 1,
    PIIType.PAN: 2,
    PIIType.IP_ADDRESS: 3,
    PIIType.EMAIL: 4,
    PIIType.DOB: 5,
    PIIType.PHONE: 6,
    PIIType.ORG: 7,      
    PIIType.PERSON: 8,
    PIIType.ADDRESS: 9,
}

def resolve_overlaps(matches: List[PIIMatch]) -> List[PIIMatch]:
    matches = sorted(matches, key=lambda m: (m.start, -(m.end - m.start)))
    resolved: List[PIIMatch] = []
    for m in matches:
        overlap_idx = None
        for i, kept in enumerate(resolved):
            if m.start < kept.end and m.end > kept.start:
                overlap_idx = i
                break
        if overlap_idx is None:
            resolved.append(m)
            continue
        kept = resolved[overlap_idx]
        m_key = (TYPE_PRIORITY.get(m.pii_type, 99), -(m.end - m.start), m.source != "regex")
        kept_key = (TYPE_PRIORITY.get(kept.pii_type, 99), -(kept.end - kept.start), kept.source != "regex")
        if m_key < kept_key:
            resolved[overlap_idx] = m
    return sorted(resolved, key=lambda m: m.start)
