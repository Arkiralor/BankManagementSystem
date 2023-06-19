from datetime import datetime
from faker import Faker
from secrets import choice
from typing import List, Set, Tuple
from os import sep, path, makedirs
from uuid import uuid4

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.utils._os import safe_join

from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress
from kyc_app.model_choices import CustomerChoice
from kyc_app.helpers import CustomerAPIHelper

from scripts import logger

ID_PROOF_FILE_PATH = safe_join(
    settings.BASE_DIR, "scripts", "data", "id_proof.jpg")
ADDRESS_PROOF_FILE_PATH = safe_join(
    settings.BASE_DIR, "scripts", "data", "address_proof.jpg")
PHOTO_FILE_PATH = safe_join(settings.BASE_DIR, "scripts", "data", "photo.jpg")


if not path.exists(ID_PROOF_FILE_PATH):
    logger.error(f"ID Proof File not found: {ID_PROOF_FILE_PATH}")
    exit(1)

if not path.exists(ADDRESS_PROOF_FILE_PATH):
    logger.error(f"Address Proof File not found: {ADDRESS_PROOF_FILE_PATH}")
    exit(1)

if not path.exists(PHOTO_FILE_PATH):
    logger.error(f"Photo File not found: {PHOTO_FILE_PATH}")
    exit(1)


class Randomizer:
    CHAR_SET: Tuple[str] = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                            "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
    DIG_SET: Tuple[str] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    ALPHANUMERIC_SET: Tuple[str] = CHAR_SET + DIG_SET
    SIZE_LIST: List[int] = [0, 1, 2, 3, 4]
    REGNAL_SUFFIXES: List[str] = ["I", "II",
                                  "III", "IV", "V", "Jr.", "Sr.", None]
    GENDER_LIST: List[str] = ["Female", "Male", "Other", "Female", "Male"]

    @classmethod
    def get_random_string(cls, length: int = 10):
        chosen_tokens = []
        for _ in range(length):
            chosen_tokens.append(
                choice(
                    list(cls.ALPHANUMERIC_SET)
                )
            )

        return "".join(chosen_tokens)

    @classmethod
    def get_random_number(cls, length: int = 10):
        chosen_tokens = []
        for _ in range(length):
            chosen_tokens.append(
                choice(
                    list(cls.DIG_SET)
                )
            )

        return "".join(chosen_tokens)

    @classmethod
    def get_random_aplhanumeric(cls, length: int = 10):
        chosen_tokens = []
        for _ in range(length):
            chosen_tokens.append(
                choice(
                    list(cls.ALPHANUMERIC_SET)
                )
            )

        return "".join(chosen_tokens)

    @classmethod
    def get_guid_str(cls):
        return uuid4().strip().replace("-", "").upper()

    @classmethod
    def assign_gender(cls):
        return choice(cls.GENDER_LIST)


class FakeFactory:

    faker: Faker = None
    middle_names: List[str] = None
    gender = None

    def __init__(self, locale: str = 'en_US', gender: str = "Female"):
        self.faker = Faker(
            locale=locale,
            providers=[
                'faker.providers.address',
                'faker.providers.bank',
                'faker.providers.person',
                'faker.providers.phone_number',
                'faker.providers.ssn',
                'faker.providers.user_agent',
                'faker.providers.company',
                'faker.providers.credit_card',
                'faker.providers.date_time',
                'faker.providers.file',
                'faker.providers.internet',
                'faker.providers.job',
                'faker.providers.lorem',
                'faker.providers.misc',
                'faker.providers.python',
                'faker.providers.barcode',
                'faker.providers.currency',
                'faker.providers.geo',
                'faker.providers.isbn',
                'faker.providers.job',
            ]
        )

        Faker.seed()
        self.randomizer = Randomizer()
        self.gender = gender.title()

    def get_middle_names(self, count: int = 1):
        middle_names = []
        if count <= 0:
            return None

        for _ in range(count):
            middle_names.append(self.faker.first_name())

        return middle_names

    def create_fake_person(self):
        first_name = self.faker.first_name_female(
        ) if self.gender == "Female" else self.faker.first_name_male()
        middle_name = self.get_middle_names(
            count=choice(self.randomizer.SIZE_LIST))
        last_name = self.faker.last_name_female(
        ) if self.gender == "Female" else self.faker.last_name_male()

        date_of_birth = self.faker.date_between_dates(
            date_start=datetime(1901, 1, 1), date_end=datetime(2001, 12, 31))
        regnal_suffix = choice(self.randomizer.REGNAL_SUFFIXES) if choice(
            [True, False]) else None

        person = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "gender": self.gender,
            "date_of_birth": date_of_birth,
            "regnal_suffix": regnal_suffix
        }

        return person

    def create_fake_kyc(self):
        id_proof_value = self.randomizer.get_random_string()
        address_proof_value = self.randomizer.get_random_string()

        kyc = {
            "id_proof_value": id_proof_value,
            "address_proof_value": address_proof_value
        }

        return kyc

    def create_address(self):
        address = {
            "address_line_1": self.faker.street_address(),
            "address_line_2": f"{self.faker.street_name()}, {self.faker.street_suffix()}",
            "city": self.faker.city(),
            "district": self.faker.city(),
            "state": self.faker.state(),
            "country": self.faker.country(),
            "pin_code": f"{choice(range(1,10))}{self.faker.zipcode()}"
        }

        return address


class FakeCustomers:

    def __init__(self):
        self.fake_factory = FakeFactory(gender=Randomizer.assign_gender())

    def assign_files(self, customer_id: str = None):
        kyc_documents = KYCDocuments.objects.filter(
            customer__pk=customer_id).first()
        if not kyc_documents:
            logger.info(f"Customer not found: {customer_id}")
            return False

        with open(ID_PROOF_FILE_PATH, "rb") as id_proof_file:
            try:
                kyc_documents.id_proof = SimpleUploadedFile(
                    "id_proof.jpg", id_proof_file.read())
                kyc_documents.id_proof_type = CustomerChoice.pan_card
                kyc_documents.save()
            except Exception as ex:
                logger.error(f"Error assigning ID Proof: {ex}")
                return False

        with open(ADDRESS_PROOF_FILE_PATH, "rb") as address_proof_file:
            try:
                kyc_documents.address_proof = SimpleUploadedFile(
                    "address_proof.jpg", address_proof_file.read())
                kyc_documents.address_proof_type = CustomerChoice.voter_id
                kyc_documents.save()
            except Exception as ex:
                logger.error(f"Error assigning Address Proof: {ex}")
                return False

        with open(PHOTO_FILE_PATH, "rb") as photo_file:
            try:
                kyc_documents.photo = SimpleUploadedFile(
                    "photo.jpg", photo_file.read())
                kyc_documents.save()
            except Exception as ex:
                logger.error(f"Error assigning Photo: {ex}")
                return False

        return True

    def fake_customer(self):
        customer = self.fake_factory.create_fake_person()
        kyc = self.fake_factory.create_fake_kyc()

        address = self.fake_factory.create_address()

        return {
            "customer": customer,
            "kyc": kyc,
            "kyc_documents": {
                "id_proof_type": CustomerChoice.pan_card,
                "address_proof_type": CustomerChoice.voter_id,
            },
            "address": address
        }

    def create_customer(self):
        data = self.fake_customer()
        customer = CustomerAPIHelper.create(data=data)
        customer_id = customer.data.get("customer", {}).get("id")
        if customer_id:
            res = self.assign_files(customer_id=customer_id)
            if not res:
                logger.error(
                    f"Error assigning files to customer: {customer_id}")
                Customer.objects.filter(pk=customer_id).delete()
                return False
            logger.info(
                f"KYC documents successfully updated for Cutomer<{customer_id}>.")

        if customer.error:
            logger.info(f"Problem creating customer: {customer.to_text()}")
            return False

        else:
            logger.info(
                f"Fake Customer created successfully: {customer.to_dict()}")
            return True


def create_customers(count: int = 1):
    if settings.ENV_TYPE != "dev" or not settings.DEBUG:
        logger.warn(
            f"ENVIRONMENT TYPE: {settings.ENV_TYPE}; DEBUG: {settings.DEBUG}")
        logger.error("This script is only for development purposes.")
        exit(1)

    for _ in range(count):
        fake_customers = FakeCustomers()
        fake_customers.create_customer()


if __name__ == "__main__":
    create_customers()
