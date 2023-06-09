from datetime import date, timedelta
from uuid import uuid4

from django.db.models import Q, QuerySet, Case, When, CharField, Value
from django.utils import timezone

from banking_app.models import Account, Transaction
from banking_app.model_choices import AccountChoice


def account_number_generator(ac_type: str = AccountChoice.savings):
    if ac_type == AccountChoice.savings:
        return f"SB{uuid4()}".replace("-", "").upper()
    elif ac_type == AccountChoice.current:
        return f"CX{uuid4()}".replace("-", "").upper()

    else:
        raise ValueError("Something went wrong.")


def get_raw_account_statement(account: Account = None, date_from: date = None, date_to: date = None, *args, **kwargs) -> QuerySet[Transaction]:

    if account is None or not isinstance(account, Account):
        raise ValueError("Invalid account provided")

    if not date_from:
        date_from = date.today() - timedelta(days=30)

    if not date_to:
        date_to = date.today()

    if (date_to - date_from) >= timedelta(days=90):
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
