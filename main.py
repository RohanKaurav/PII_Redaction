#!/usr/bin/env python3
import sys
import csv
from collections import Counter
from pathlib import Path

from pii_redaction import (
    extract_pages,
    load_ner_model,
    FakeMapper,
    run_all_detectors,
    redact_page_text
)

def main(pdf_path: str, output_txt: str, audit_csv: str):
    print(f"Extracting text from {pdf_path} ...")
    pages = extract_pages(pdf_path)
    print(f"Extracted {len(pages)} pages.")

    print("Loading NER model ...")
    nlp = load_ner_model()

    mapper = FakeMapper()
    redacted_pages = []
    audit_rows = []

    for page_num, text in enumerate(pages, start=1):
        matches = run_all_detectors(text, page_num, nlp)
        redacted_text = redact_page_text(text, matches, mapper)
        redacted_pages.append(redacted_text)

        for m in matches:
            audit_rows.append(
                {
                    "page": page_num,
                    "pii_type": m.pii_type.value,
                    "original": m.text,
                    "redacted_as": mapper.get_fake(m.text, m.pii_type),
                    "detection_method": m.source,
                }
            )

        if page_num % 20 == 0:
            print(f"  processed page {page_num}/{len(pages)}")

    Path(output_txt).write_text("\n\f\n".join(redacted_pages), encoding="utf-8")
    print(f"Redacted text written to {output_txt}")

    with open(audit_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["page", "pii_type", "original", "redacted_as", "detection_method"]
        )
        writer.writeheader()
        writer.writerows(audit_rows)
    print(f"Audit log written to {audit_csv} ({len(audit_rows)} redactions)")

    counts = Counter(r["pii_type"] for r in audit_rows)
    print("\nRedaction counts by type:")
    for t, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {t:20s}: {c}")

if __name__ == "__main__":
    pdf_arg = sys.argv[1] if len(sys.argv) > 1 else "Red_Herring_Prospectus.pdf"
    out_arg = sys.argv[2] if len(sys.argv) > 2 else "redacted_output.txt"
    audit_arg = sys.argv[3] if len(sys.argv) > 3 else "audit_log.csv"
    main(pdf_arg, out_arg, audit_arg)
