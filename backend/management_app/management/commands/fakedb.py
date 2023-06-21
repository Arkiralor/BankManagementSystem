from django.core.management.base import BaseCommand

from scripts.create_customers import create_customers
from scripts.create_accounts import create_accounts

from core import logger


class Command(BaseCommand):
    """
    Management command to create fake data in the database.
    """
    help = 'Fake database'

    amount = 10

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int,
                            help='Amount of customers to create')

    def handle(self, *args, **options):
        self.amount = int(
            options['amount']) if options['amount'] else self.amount

        try:
            logger.info('Creating customers...')
            create_customers(self.amount)
            logger.info('Creating accounts...')
            create_accounts(int(self.amount//2))
            logger.info('Done!')
        except Exception as ex:
            logger.error(ex)

    def log(self, message):
        self.stdout.write(message)
