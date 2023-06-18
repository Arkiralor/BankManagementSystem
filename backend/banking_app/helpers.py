from datetime import date, timedelta
from typing import List

from django.db.models import Q, QuerySet, Case, When, CharField, Value
from django.utils import timezone

from rest_framework import status

from core.boilerplate.response_template import Resp
from banking_app.models import Account, Transaction
from banking_app.model_choices import AccountChoice, TransactionChoice
from banking_app.serializers import AccountInputSerializer, TransactionInputSerializer, TransactionOutputSerializer, AccountOutputSerializer
from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress
from kyc_app.serializers import CustomerSerializer, KYCDocumentsInputSerializer, KYCDocumentsOutputSerializer, KnowYourCustomerInputSerializer, \
    KnowYourCustomerOutputSerializer, CustomerAddressInputSerializer, CustomerAddressOutputSerializer

from banking_app import logger


class AccountHelpers:
    MIN_DEPOSIT: float = 10_000.00

    @classmethod
    def get(cls, account_id: str = None):
        return Account.objects.filter(pk=account_id).first()

    @classmethod
    def retrieve(cls, account_number: str = None, customer_id: str = None, *args, **kwargs) -> Resp:
        """
        Retreive the details of a single bank account or all accounts belonging to an individual customer.
        """
        resp = Resp()

        if (not account_number or account_number == "") and (not customer_id or customer_id == ""):
            resp.error = "Invalid Account Number or Customer ID"
            resp.message = f"Account Number: {account_number} | Customer ID: {customer_id}"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        accounts= Account.objects.filter(
            Q(account_number__iexact=account_number)
            | Q(holder__pk=customer_id)
        ).order_by("-created")

        serialized = AccountOutputSerializer(accounts, many=True).data

        resp.message = "Account Retrieved Successfully"
        resp.data = serialized
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp

    @classmethod
    def check_customer(cls, customer: Customer = None, *args, **kwargs) -> bool:
        """
        Check if the customer is valid i.e, their KYC (Know Your Customer) details are all in order.
        """
        kyc = KnowYourCustomer.objects.filter(customer=customer).first()
        if kyc is None:
            logger.warn(f"KYC details not found for customer {customer.id}")
            return False
        kyc_documents = KYCDocuments.objects.filter(customer=customer).first()
        if kyc_documents is None:
            logger.warn(f"KYC documents not found for customer {customer.id}")
            return False
        customer_address = CustomerAddress.objects.filter(
            customer=customer).first()
        if customer_address is None:
            logger.warn(
                f"Customer address not found for customer {customer.id}")
            return False

        is_valid = (kyc.address_proof_value and kyc.id_proof_value) and (
            kyc_documents.address_proof and kyc_documents.id_proof and kyc_documents.photo) and customer_address.pin_code

        return bool(is_valid)

    @classmethod
    def create(cls, customers: List[Customer] = None, balance: float = 0.0, account_type: str = AccountChoice.savings, *args, **kwargs) -> Resp:
        """
        Create a new account for a given customer.
        """
        resp = Resp()
        if customers is None:
            resp.error = "Invalid customer provided"
            resp.message = "Please provide a valid customer for the account holder."
            resp.data = None
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        for customer in customers:
            if not cls.check_customer(customer=customer):
                resp.error = "KYC details not found"
                resp.message = "Please complete the KYC procedure for the customer first."
                resp.data = {
                    "customer": CustomerSerializer(customer).data,
                }
                resp.status_code = status.HTTP_400_BAD_REQUEST

                logger.warn(resp.message)
                return resp

        if balance < cls.MIN_DEPOSIT:
            resp.error = "Invalid deposit amount"
            resp.message = f"Minimum deposit amount is {cls.MIN_DEPOSIT}"
            resp.data = {
                "customer": f"{[str(customer) for customer in customers]}",
                "account_type": account_type,
                "balance": balance
            }
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        data = {
            "holder": [customer.id for customer in customers],
            "account_type": account_type,
            "balance": balance
        }

        deserialized = AccountInputSerializer(data=data)
        if not deserialized.is_valid():
            resp.error = "Invalid account data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        deserialized.save()

        resp.message = f"Account {deserialized.instance} created successfully."
        resp.data = AccountOutputSerializer(deserialized.instance).data
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp
    
    @classmethod
    def get_statement(cls, account: Account = None, date_from: date = None, date_to: date = None, *args, **kwargs) -> Resp:
        """
        Retrieve the account statement for a given account.
        """
        resp = Resp()

        if account is None or not isinstance(account, Account):
            resp.error = "Invalid Account"
            resp.message = f"Account: {account}"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        transactions = TransactionHelpers.get_account_transactions(account=account, date_from=date_from, date_to=date_to)
        serialized = TransactionOutputSerializer(transactions, many=True).data

        resp.message = "Account Statement Retrieved Successfully"
        resp.data = serialized
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp


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
