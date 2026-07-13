from dataclasses import dataclass
from enum import Enum

class PIIType(str, Enum):
    PERSON = "PERSON_NAME"
    EMAIL = "EMAIL"
    PHONE = "PHONE_NUMBER"
    ORG = "COMPANY_NAME"
    ADDRESS = "ADDRESS"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    DOB = "DATE_OF_BIRTH"
    IP_ADDRESS = "IP_ADDRESS"
    PAN = "PAN_NUMBER" 

@dataclass
class PIIMatch:
    start: int
    end: int
    text: str
    pii_type: PIIType
    page: int
    source: str  
