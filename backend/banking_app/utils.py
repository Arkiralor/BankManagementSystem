
from uuid import uuid4

from banking_app.model_choices import AccountChoice


def account_number_generator(ac_type: str = AccountChoice.savings) -> str:
    return f"{uuid4().hex.upper()}"


