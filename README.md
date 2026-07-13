# PII Redaction Tool

This tool reads a PDF document and produces a redacted text version where Personally Identifiable Information (PII) is replaced with consistent, realistic fake values.

## Features
- **Structured PII Detection**: Uses regex for predictable formats (Email, Phone, SSN, Credit Card, IP, PAN, DOB).
- **Unstructured PII Detection**: Uses spaCy NER for names, organizations, and addresses.
- **Context-Aware Filters**: Specifically tuned to avoid over-redacting regulatory bodies, legal defined terms, and Indian corporate nomenclature common in financial filings.
- **Consistent Fake Data**: Uses Faker with deterministic hashing to ensure the same real entity is replaced by the same fake entity throughout the document.
- **Audit Logging**: Generates a CSV file detailing every redaction made.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the spaCy NER model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the main script with the target PDF, output text file, and audit log CSV file as arguments:

```bash
python main.py [input.pdf] [output.txt] [audit.csv]
```

### Example

```bash
python main.py Example.pdf redacted.txt audit.csv
```

## Configuration
Stop-lists and allow-lists tailored for specific document types (like Indian prospectuses) can be modified in `pii_redaction/config.py`.

## Approach
This tool uses a hybrid approach to maximize both precision and recall when redacting PII:
1. **Regex-based Detection**: Used for structured PII with predictable formats (like Emails, Phone Numbers, SSNs, Credit Cards, IPs, and Indian PANs). Regular expressions provide high precision and fast matching for these fixed formats.
2. **NER Model (spaCy)**: Employed for unstructured PII that lacks fixed patterns, such as Person Names, Company Names, and Addresses. The generic `en_core_web_sm` model is used, which works well out-of-the-box but is supplemented with domain-specific filters.
3. **Third-Party Libraries**: `pdfplumber` is used for robust text extraction from PDFs, and `Faker` is used to deterministically generate consistent replacement data.

## Tradeoffs and Limitations
- **False Positives**: The generic NER model frequently mislabels capitalized defined terms (e.g., "The Offer", "The Board", "Draft Red Herring Prospectus") and field labels as organizations or names. To mitigate this, a curated stoplist of common legal terms is used. Conversely, aggressive filtering can cause false negatives if a real name overlaps with a stoplist term.
- **False Negatives**: The NER model often struggles to identify names written in ALL-CAPS text blocks. To handle this, the text is processed in two passes (original and title-cased), but some highly unusual names or broken text from PDF formatting might still be missed.
- **Regex Limitations**: Phone numbers that are split across multiple lines due to PDF table artifacts can evade regex matching. A heuristic to rejoin dangling digits is included, but it may not catch complex multi-line splits.

## Evaluation Approach
The evaluation strategy focuses on targeted precision and recall checks using the generated audit log (`audit.csv`).
- **Precision**: Evaluated by reviewing the audit log to ensure the extracted text truly belongs to its labeled category (e.g. verifying that a detected `COMPANY_NAME` isn't actually a generic legal term or boilerplate text). 
- **Recall**: Evaluated manually by reading samples of the output text side-by-side with the original PDF to spot PII that slipped past the regex patterns and NER model. The dual-pass NER (title-casing) and line-rejoining heuristics were implemented directly in response to these manual recall checks.
