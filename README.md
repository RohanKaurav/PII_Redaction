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
python main.py Red_Herring_Prospectus.pdf redacted.txt audit.csv
```

## Configuration
Stop-lists and allow-lists tailored for specific document types (like Indian prospectuses) can be modified in `pii_redaction/config.py`.
