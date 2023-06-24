from django.core.management.base import BaseCommand

from banking_app.models import Account, Transaction
from kyc_app.models import Customer

from core import logger


class Command(BaseCommand):
    """
    Management command to clear fake data in the database.
    """
    help: str = 'Clear fake data in the database, namely customers, accounts and transactions.'

    def handle(self, *args, **options):
        try:
            customers = Customer.objects.all()
            accounts = Account.objects.all()
            transactions = Transaction.objects.all()

            logger.info('Deleting transactions...')
            transactions.delete()
            logger.info('Deleting accounts...')
            accounts.delete()
            logger.info('Deleting customers...')
            customers.delete()
        except Exception as ex:
            logger.error(ex)

        logger.info('Done!')

    def log(self, message):
        self.stdout.write(message)
