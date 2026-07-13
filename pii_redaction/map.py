import re
import hashlib
from faker import Faker
from .types import PIIType

class FakeMapper:
    def __init__(self):
        self.cache: dict[tuple[PIIType, str], str] = {}

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    @staticmethod
    def _seed_for(pii_type: PIIType, normalized: str) -> int:
        h = hashlib.sha256(f"{pii_type}:{normalized}".encode()).hexdigest()
        return int(h[:8], 16)

    def get_fake(self, real_text: str, pii_type: PIIType) -> str:
        key = (pii_type, self._normalize(real_text))
        if key in self.cache:
            return self.cache[key]

        faker = Faker()
        faker.seed_instance(self._seed_for(pii_type, key[1]))

        if pii_type == PIIType.PERSON:
            fake = faker.name()
        elif pii_type == PIIType.EMAIL:
            fake = faker.email()
        elif pii_type == PIIType.PHONE:
            fake = faker.phone_number()
        elif pii_type == PIIType.ORG:
            fake = faker.company()
        elif pii_type == PIIType.ADDRESS:
            fake = faker.city()
        elif pii_type == PIIType.SSN:
            fake = faker.ssn()
        elif pii_type == PIIType.CREDIT_CARD:
            fake = faker.credit_card_number()
        elif pii_type == PIIType.DOB:
            fake = faker.date_of_birth().strftime("%d-%m-%Y")
        elif pii_type == PIIType.IP_ADDRESS:
            fake = faker.ipv4()
        elif pii_type == PIIType.PAN:
            fake = (
                "".join(faker.random_uppercase_letter() for _ in range(5))
                + "".join(str(faker.random_digit()) for _ in range(4))
                + faker.random_uppercase_letter()
            )
        else:
            fake = "[REDACTED]"

        self.cache[key] = fake
        return fake
