from django.db.models.signals import post_save

from banking_app.models import Account, Transaction
from banking_app import logger


class AccountSignalReciever:
    model = Account

    @classmethod
    def post_save(cls, sender, instance:Account, created, *args, **kwargs):
        if created:
            logger.info(f"Account {instance.account_number} created. Initial balance: {instance.balance}")

        else:
            logger.info(f"Account {instance.account_number} updated. Available balance: {instance.balance}")

post_save.connect(receiver=AccountSignalReciever.post_save, sender=AccountSignalReciever.model)

class TransactionSignalReciever:
    model = Transaction

    @classmethod
    def post_save(cls, sender, instance:Transaction, created, *args, **kwargs):
        if created:
            if instance.source:
                instance.source.debit(amount=instance.amount)
            if instance.destination:
                instance.destination.credit(amount=instance.amount)


post_save.connect(receiver=TransactionSignalReciever.post_save, sender=TransactionSignalReciever.model)