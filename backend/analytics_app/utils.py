from datetime import datetime, date, timedelta

from django.db.models import Q, QuerySet, Count, When, Value, Case, Func
from django.db.models.functions import ExtractYear
from django.utils import timezone

from banking_app.models import Account, Transaction
from banking_app.model_choices import AccountChoice, TransactionChoice
from kyc_app.models import Customer
from kyc_app.model_choices import CustomerChoice

from analytics_app import logger


class CustomerAnalyticsUtils:

    @classmethod
    def get_customer_age_groups(cls):

        try:
            customers = Customer.objects.all().annotate(
                age=Case(
                    When(date_of_birth__isnull=True, then=Value(0)),
                    default=timezone.now().year - ExtractYear("date_of_birth")
                )
            ).annotate(
                age_group=Case(
                    When(age__gte=0, age__lte=17, then=Value("0-17")),
                    When(age__gte=18, age__lte=25, then=Value("18-25")),
                    When(age__gte=26, age__lte=35, then=Value("26-35")),
                    When(age__gte=36, age__lte=45, then=Value("36-45")),
                    When(age__gte=46, age__lte=55, then=Value("46-55")),
                    When(age__gte=56, age__lte=65, then=Value("56-65")),
                    When(age__gte=66, age__lte=75, then=Value("66-75")),
                    When(age__gte=76, age__lte=85, then=Value("76-85")),
                    When(age__gte=86, then=Value("86+")),
                    default=Value("Unknown")
                )
            ).values("age_group").annotate(count=Count("age_group")).order_by("age_group")

        except Exception as ex:
            logger.info(f"Error fetching customer age groups: {ex}")
            return None

        return customers

    @classmethod
    def get_customers_by_gender(cls):

        try:
            customers = Customer.objects.all().annotate(
                group=Case(
                    When(gender__isnull=True, then=Value("Unknown")),
                    When(gender=CustomerChoice.female, then=Value("Female")),
                    When(gender=CustomerChoice.male, then=Value("Male")),
                    When(gender=CustomerChoice.other, then=Value("Other"))
                )
            ).values("group").annotate(count=Count("group")).order_by("group")
        except Exception as ex:
            logger.warn(f"Error fetching customer gender groups: {ex}")
            return None

        return customers


class TransactionAnalyticsUtils:

    @classmethod
    def get_transactions_by_type(cls):

        try:
            transactions = Transaction.objects.all().annotate(
                group=Case(
                    When(transaction_type=TransactionChoice.cash_deposit, then=Value("Cash Deposit")),
                    When(transaction_type=TransactionChoice.account_transfer, then=Value("Account Transfer")),
                    When(transaction_type=TransactionChoice.withdrawal, then=Value("Account Withdrawal")),
                    default=Value("Unknown")
                )
            ).values("group").annotate(count=Count("group")).order_by("group")
        except Exception as ex:
            logger.warn(f"Error fetching transaction type groups: {ex}")
            return None

        return {
            "total": transactions.count(),
            "transactions": transactions,
        }
    
    @classmethod
    def get_transaction_by_amount(cls):
        try:
            transactions = Transaction.objects.all().annotate(
                group=Case(
                    When(amount__gte=0, amount__lte=500, then=Value("a. 0-500")),
                    When(amount__gte=501, amount__lte=1_000, then=Value("b. 501-1'000")),
                    When(amount__gte=1_001, amount__lte=1_500, then=Value("c. 1'001-1'500")),
                    When(amount__gte=1_501, amount__lte=2_000, then=Value("d. 1'501-2'000")),
                    When(amount__gte=2_001, amount__lte=2_500, then=Value("e. 2'001-2'500")),
                    When(amount__gte=2_501, amount__lte=3_000, then=Value("f. 2'501-3'000")),
                    When(amount__gte=3_001, amount__lte=3_500, then=Value("g. 3'001-3'500")),
                    When(amount__gte=3_501, amount__lte=4_000, then=Value("h. 3'501-4'000")),
                    When(amount__gte=4_001, amount__lte=4_500, then=Value("i. 4'001-4'500")),
                    When(amount__gte=4_501, amount__lte=5_000, then=Value("j. 4'501-5'000")),
                    When(amount__gte=5_001, amount__lte=10_000, then=Value("k. 5'001-10'000")),
                    When(amount__gte=10_001, amount__lte=50_000, then=Value("l. 10'001-50'000")),
                    When(amount__gte=50_001, amount__lte=100_000, then=Value("m. 50'001-100'000")),
                    When(amount__gte=100_001, amount__lte=500_000, then=Value("n. 100'001-500'000")),
                    When(amount__gte=500_001, amount__lte=1_000_000, then=Value("o. 500'001-1'000'000")),
                    When(amount__gte=1_000_001, amount__lte=5_000_000, then=Value("p. 1'000'001-5'000'000")),
                    When(amount__gte=5_000_001, amount__lte=10_000_000, then=Value("q. 5'000'001-10'000'000")),
                    When(amount__gte=10_000_001, amount__lte=50_000_000, then=Value("r. 10'000'001-50'000'000")),
                    When(amount__gte=50_000_001, amount__lte=100_000_000, then=Value("s. 50'000'001-100'000'000")),
                    When(amount__gte=100000001, then=Value("t. 10000000+")),
                    default=Value("u. Unknown")
                )
            ).values("group").annotate(count=Count("group")).order_by("group")

        except Exception as ex:
            logger.warn(f"Error fetching transaction amount groups: {ex}")
            return None
        
        return {
            "total": transactions.count(),
            "transactions": transactions,
        }
    
    @classmethod
    def get_transactions_by_date(cls):
        try:
            transactions = Transaction.objects.all().annotate(
                group=Case(
                    When(created__gte=(timezone.now() - timedelta(days=1)), then=Value("a. Today")),
                    When(created__gte=(timezone.now() - timedelta(days=7)), then=Value("b. Last 7 days")),
                    When(created__gte=(timezone.now() - timedelta(days=30)), then=Value("c. Last 30 days")),
                    When(created__gte=(timezone.now() - timedelta(days=90)), then=Value("d. Last 90 days")),
                    When(created__gte=(timezone.now() - timedelta(days=180)), then=Value("e. Last 180 days")),
                    When(created__gte=(timezone.now() - timedelta(days=365)), then=Value("f. Last 365 days")),
                    default=Value("g. Older than 365 days")
                )
            ).values("group").annotate(count=Count("group")).order_by("group")

        except Exception as ex:
            logger.warn(f"Error fetching transaction date groups: {ex}")
            return None
        
        return {
            "total": transactions.count(),
            "transactions": transactions,
        }
        
