from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from scripts.create_customers import create_customers
from scripts.create_accounts import create_accounts
from scripts.create_transactions import create_transactions

from core import logger


class Command(BaseCommand):
    """
    Management command to create fake data in the database.

    Usage:
        python manage.py fakedb --amount 10 --test True
    """
    help: str = 'Create fake data in the database, namely customers and accounts.'

    amount: int = 10
    test: bool = False

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--amount',
            type=int,
            help='Amount of customers to create',
            default=self.amount
        )
        parser.add_argument(
            '--test', 
            type=bool,
            help='Whether to just check if the command is recognised.'
        )

    def handle(self, *args, **options):
        self.amount = options.get('amount') if options.get('amount') else self.amount
        self.test = options.get('test') if options.get('test') else self.test

        if self.test == True:
            logger.info(f"SELF.test = {self.test}")
            logger.info('Creating fake database entries (Testing)...')
            return 
            

        try:
            logger.info('Creating customers...')
            create_customers(self.amount)
            logger.info('Creating accounts...')
            create_accounts(int(self.amount//2))
            logger.info('Creating transactions...')
            create_transactions(int(self.amount*2))
            logger.info(f"Fake database entries created.")
        except Exception as ex:
            logger.error(ex)

        logger.info('Done!')

    def log(self, message):
        self.stdout.write(message)
