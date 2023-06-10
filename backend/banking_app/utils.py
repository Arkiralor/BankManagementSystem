
from uuid import uuid4

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


