from datetime import date, timedelta
from uuid import uuid4

from django.db.models import Q, QuerySet, Case, When, CharField, Value
from django.utils import timezone

from banking_app.models import Account, Transaction
from banking_app.model_choices import AccountChoice


def account_number_generator(ac_type: str = AccountChoice.savings) -> str:
    account_type_prefixes = {
        AccountChoice.savings: "SB",
        AccountChoice.current: "CX",
        AccountChoice.loan: "LN",
        AccountChoice.credit: "CR",
    }

    prefix = account_type_prefixes.get(ac_type)
    if prefix is None:
        raise ValueError("Invalid account type")

    return f"{prefix}{uuid4().hex.upper()}"


def get_account_transactions(account: Account = None, date_from: date = None, date_to: date = None, *args, **kwargs) -> QuerySet[Transaction]:

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
