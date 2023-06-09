from django.db import models

from core.boilerplate.model_template import TemplateModel
from banking_app.model_choices import AccountChoice
from banking_app.utils import account_number_generator
from kyc_app.models import Customer

class Account(TemplateModel):
    ## The ID is for internal referencing (within the backend);
    ## The Account Number is for external referencing (outside the backend).
    account_number = models.CharField(unique=True, default=account_number_generator, editable=False)
    holder = models.ManyToManyField(Customer)
    balance = models.DecimalField(decimal_places=2)
    account_type = models.CharField(max_length=16, choices=AccountChoice.ACCOUNT_TYPES)

    def credit(self, amount:float, *args, **kwargs):
        self.balance = self.balance + amount
        self.save()

    def debit(self, amount:float, *args, **kwargs):
        self.balance = self.balance - amount
        self.save()

class Transaction(TemplateModel):
    source = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    destination = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.source.debit(amount=self.amount)
        self.destination.credit(amount=self.amount)

        super(Transaction, self).__init__(*args, **kwargs)