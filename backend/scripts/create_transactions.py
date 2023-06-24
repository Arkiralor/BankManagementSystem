from datetime import datetime, timedelta
from secrets import choice

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from banking_app.models import Account, Transaction
from banking_app.model_choices import TransactionChoice
from banking_app.helpers import TransactionHelpers
from user_app.models import User
from user_app.model_choices import UserModelChoices

from scripts import logger

ACCOUNTS = Account.objects.all()
TELLERS = User.objects.filter(user_type=UserModelChoices.teller)

class FakeTransaction:
    source: Account
    destination: Account
    amount: float
    txn_id: str

    def __init__(self):
        self.source = choice(ACCOUNTS)
        self.destination = choice(ACCOUNTS.filter(~Q(pk=self.source.id)))
        self.amount = choice(range(1, int(self.source.balance//1000)))

    def transaction(self):
        if self.destination.balance <=10_000:
            logger.warn(f"Destination account {self.destination} has low balance.")
            return False
        try:            
            resp = TransactionHelpers.create(
                source_id=f"{self.source.id}",
                destination_id=f"{self.destination.id}",
                amount=self.amount,
                authorised_by=choice(TELLERS),
                transaction_type=TransactionChoice.account_transfer
            )

            if resp.error:
                logger.warn(resp.to_text())

            self.txn_id = resp.data.get("id")
        except Exception as ex:
            logger.error(f"Error creating transaction: {ex}")
            return False

        return True
    
    def backdate(self):
        if not self.txn_id:
            logger.error("Transaction not created.")
            return False
        
        try:
            txn_obj = Transaction.objects.get(pk=self.txn_id)
            txn_obj.created = timezone.now() - timedelta(days=choice(range(1, 3650)))
            txn_obj.save()
        except Exception as ex:
            logger.error(f"Error backdating transaction: {ex}")
            return False

def create_transactions(count: int = 1):
    if settings.ENV_TYPE != "dev" or not settings.DEBUG:
        logger.warn(
            f"ENVIRONMENT TYPE: {settings.ENV_TYPE}; DEBUG: {settings.DEBUG}")
        logger.error("This script is only for development purposes.")
        exit(1)
        
    for i in range(count):
        transaction = FakeTransaction()
        res = transaction.transaction()
        if res:
            logger.info(f"Transaction {i + 1} created")
        
        res = transaction.backdate()
        if res:
            logger.info(f"Transaction {i + 1} backdated")
        


if __name__ == "__main__":
    create_transactions(100)