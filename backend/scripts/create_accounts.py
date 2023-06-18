from secrets import choice

from django.conf import settings

from banking_app.helpers import AccountHelpers
from banking_app.model_choices import AccountChoice
from kyc_app.models import Customer

from scripts import logger


class FakeAccount:

    CUSTOMERS = Customer.objects.all()
    NUMBER_OF_HOLDERS = [1, 2, 3, 4, 5]
    TYPES_OF_ACCOUNTS = [AccountChoice.savings,
                         AccountChoice.current, AccountChoice.loan, AccountChoice.credit]

    @classmethod
    def get_account_holders(cls, count=1):
        if count <= 0:
            raise ValueError(
                "There cannot be 0 account holders for an account.")

        holders = []
        for _ in range(count):
            holders.append(choice(cls.CUSTOMERS))

        return holders

    @classmethod
    def create_account(cls):
        account_type = choice(cls.TYPES_OF_ACCOUNTS)
        holder = cls.get_account_holders(choice(cls.NUMBER_OF_HOLDERS))
        balance = choice(range(10_000, 2_500_000, 1))

        resp = AccountHelpers.create(customers=holder, balance=float(
            balance), account_type=account_type)
        if resp.error:
            logger.warn(resp.to_text())
        else:
            logger.info(f"Fake Bank Account created: {resp.to_dict()}")


def main(count: int = 1):
    if settings.ENV_TYPE != "dev" or not settings.DEBUG:
        logger.warn(
            f"ENVIRONMENT TYPE: {settings.ENV_TYPE}; DEBUG: {settings.DEBUG}")
        logger.error("This script is only for development purposes.")
        exit(1)

    for _ in range(count):
        FakeAccount.create_account()


if __name__ == "__main__":
    main()
