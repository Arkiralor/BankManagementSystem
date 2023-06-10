from django.db import models

from core.boilerplate.model_template import TemplateModel
from banking_app.model_choices import AccountChoice, TransactionChoice
from banking_app.utils import account_number_generator
from kyc_app.models import Customer

class Account(TemplateModel):
    ## The ID is for internal referencing (within the backend);
    ## The Account Number is for external referencing (outside the backend).
    account_number = models.CharField(unique=True, default=account_number_generator, editable=False)
    holder = models.ManyToManyField(Customer)
    balance = models.DecimalField(max_digits=16, decimal_places=2)
    account_type = models.CharField(max_length=16, choices=AccountChoice.ACCOUNT_TYPES)

    def __str__(self):
        return self.account_number

    def credit(self, amount:float, *args, **kwargs):
        self.balance = self.balance + amount
        self.save()

    def debit(self, amount:float, *args, **kwargs):
        self.balance = self.balance - amount
        self.save()

    
    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
        ordering = ("-created",)

class Transaction(TemplateModel):
    source = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name="source_account")
    destination = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name="destination_account")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_type = models.CharField(max_length=128, choices=TransactionChoice.TRANSACTION_TYPE)

    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.source:
                self.source.debit(amount=self.amount)
            if self.destination:
                self.destination.credit(amount=self.amount)

        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-created",)