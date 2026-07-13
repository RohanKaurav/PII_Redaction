from .types import PIIType

NER_LABEL_MAP = {
    "PERSON": PIIType.PERSON,
    "ORG": PIIType.ORG,
    "GPE": PIIType.ADDRESS,   # cities/states/countries -> treated as address fragments
    "LOC": PIIType.ADDRESS,
    "FAC": PIIType.ADDRESS,   # named facilities/buildings
}

# Regulatory/statutory bodies & legal references: excluded from ORG redaction.
ORG_ALLOWLIST = {
    "sebi", "rbi", "nse", "bse", "roc", "reserve bank of india",
    "securities and exchange board of india", "registrar of companies",
    "companies act", "income tax act", "it act", "fema",
    "sebi icdr regulations", "gst", "national stock exchange",
    "bombay stock exchange", "depositories act", "sebi act",
    "maharashtra", "gujarat",
}

# Short all-caps field-label acronyms that spaCy occasionally mistags as ORG
FIELD_LABEL_ALLOWLIST = {
    "ssn", "pan", "dob", "ip", "cin", "gst", "tan", "kyc", "ifsc",
    "rtgs", "neft", "upi", "ocr", "ein",
}

# Broad stoplist for legal/defined terms
DEFINED_TERM_STOPLIST = {
    "offer", "bid", "bids", "bidders", "directors", "promoters", "board",
    "company", "prospectus", "registrar", "syndicate", "allotment",
    "equity", "equity share", "equity shares", "shares", "mutual funds",
    "anchor investors", "non-institutional investors",
    "retail individual investors", "qualified institutional buyers",
    "promoter group", "statutory auditors", "designated intermediaries",
    "registered office", "corporate office", "asba", "asba forms",
    "asba account", "asba bidders", "icdr regulations",
    "icdr master circular", "ind as", "scsbs", "scsb", "underwriters",
    "bankers", "trade", "moa", "cfo", "cs", "ctc", "mt", "llp",
    "group companies", "working days", "bonus", "issuer", "fresh",
    "operations", "cogs", "pat", "capital employed", "capital structure",
    "financial information", "senior management",
    "key managerial personnel", "executive directors",
    "independent directors", "individual promoters", "first bidder",
    "basis of allotment", "non-resident", "cdp", "mip", "email", "tel",
    "particulars", "share transfer agents", "upi bidders", "up", "rw",
    "du", "currency", "opens", "bid/offer closing day",
    "red herring prospectus", "draft red herring prospectus",
    "inter alia", "non-institutional portion", "cap price", "roc",
}

# Standalone country/nation-level references
COUNTRY_LEVEL_STOPLIST = {
    "india", "us", "u.s.", "usa", "sweden",
    "the united states", "the united states of america",
    "the republic of india", "hindi", "yojana",
}
