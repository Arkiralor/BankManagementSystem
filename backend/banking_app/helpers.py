from datetime import date, timedelta

from django.db.models import Q, QuerySet, Case, When, CharField, Value
from django.utils import timezone

from banking_app.models import Account, Transaction

class TransactionHelpers:

    MAX_DATE_RANGE: int = 90

    @classmethod
    def get_account_transactions(cls, account: Account = None, date_from: date = None, date_to: date = None, *args, **kwargs) -> QuerySet[Transaction]:

        if account is None or not isinstance(account, Account):
            raise ValueError("Invalid account provided")

        if not date_from:
            date_from = date.today() - timedelta(days=30)

        if not date_to:
            date_to = date.today()

        if (date_to - date_from) >= timedelta(days=cls.MAX_DATE_RANGE):
            date_to = date.today()
            date_from = date_to - timedelta(days=30)

        transactions = Transaction.objects.filter(
            Q(
                Q(source=account)
                | Q(destination=account)
            )
            & Q(created__date__range=(date_from, date_to))
        ).annotate(
            transaction_type=Case(
                When(source=account, then=Value('Debit')),
                When(destination=account, then=Value('Credit')),
                default=Value('Unknown'),
                output_field=CharField(),
            )
        ).order_by("-created")

        return transactions
