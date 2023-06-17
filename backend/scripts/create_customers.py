from faker import Faker
from secrets import choice
from typing import List

from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress


class FakeFactory:

    faker: Faker = None
    middle_names: List[str] = None
    gender = None

    def __init__(self, locale: str = 'en_US', gender:str = "Female"):
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
    
        Faker.seed(0)
        self.gender = gender.title()
        
    def get_middle_names(self, count: int = 1):
        return list(set(choice(self.middle_names, count)))

    def create_fake_person(self):
        first_name = self.faker.first_name_female() if self.gender == "Female" else self.faker.first_name_male()
        last_name = self.faker.last_name_female() if self.gender == "Female" else self.faker.last_name_male()


class FakeCustomers:

    pass
