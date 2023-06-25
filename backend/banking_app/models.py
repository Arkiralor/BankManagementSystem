"""
Module to store models used in the `banking_app`.
"""

from django.db import models

from core.boilerplate.model_template import TemplateModel
from banking_app.model_choices import AccountChoice, TransactionChoice
from banking_app.utils import account_number_generator
from kyc_app.models import Customer
from user_app.models import User


class Account(TemplateModel):
    """
    Model to store information about a single bank account.
    """
    account_type = models.CharField(
        max_length=16, choices=AccountChoice.ACCOUNT_TYPES)
    # The ID is for internal referencing (within the backend);
    # The Account Number is for external referencing (outside the backend).
    account_number = models.CharField(
        unique=True, default=account_number_generator, editable=False)
    holder = models.ManyToManyField(Customer)
    balance = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        """
        `.str()` method for the class.
        """
        return f"{self.account_number}"

    def save(self, *args, **kwargs):
        """
        Overloaded `model.save()` method.
        """
        super(Account, self).save(*args, **kwargs)

    def credit(self, amount: float = 0.0, *args, **kwargs):
        """
        Method to credit the account with the given amount.
        """
        self.balance = self.balance + amount
        self.save()

    def debit(self, amount: float = 0.0, *args, **kwargs):
        """
        Method to debit the account with the given amount.
        """
        self.balance = self.balance - amount
        self.save()

    class Meta:
        """
        Meta options for the class.
        """
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
        ordering = ("-created",)

        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('account_number',)),
        )


class Transaction(TemplateModel):
    """
    Model to hold information regarding bankaccount transactions.
    """
    source = models.ForeignKey(Account, on_delete=models.SET_NULL,
                               blank=True, null=True, related_name="source_account")
    destination = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name="destination_account")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_type = models.CharField(
        max_length=128, choices=TransactionChoice.TRANSACTION_TYPE)
    authorised_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """
        `.str()` method for the class.
        """
        return f"{self.pk}"

    def save(self, *args, **kwargs):
        """
        Overloaded `model.save()` method.
        """
        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        """
        Meta options for the class.
        """
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-created",)

        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('destination', 'source')),
        )
