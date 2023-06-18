from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.permissions import IsAccountantOrTeller, IsModerator
from core.boilerplate.response_template import Resp
from banking_app.helpers import AccountHelpers, TransactionHelpers
from kyc_app.helpers import CustomerAPIHelper


class BankAccountAPI(APIView):
    permission_classes = (IsAccountantOrTeller | IsAdminUser,)

    def get(self, request: Request, *args, **kwargs):
        """
        Retreive the details of a single bank account or all accounts belonging to an individual customer.
        """
        account_number = request.query_params.get("account")
        customer_id = request.query_params.get("customer")

        resp = AccountHelpers.retrieve(
            account_number=account_number, customer_id=customer_id)
        return resp.to_response()

    def post(self, request: Request, *args, **kwargs):
        """
        Create a new account for a given customer.
        """

        data = request.data

        customer_ids = data.get("customers", [])
        customers = [CustomerAPIHelper.get(customer_id=individual_id) for individual_id in customer_ids]

        balance = data.get("deposit")
        account_type = data.get("type")

        resp = AccountHelpers.create(
            customers=customers, balance=balance, account_type=account_type)
        return resp.to_response()
    

class TransactionAPI(APIView):
    permission_classes = (IsAccountantOrTeller | IsAdminUser,)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        source = data.get("source")
        destination = data.get("destination")
        amount = data.get("amount")
        transaction_type = data.get("type")

        resp = TransactionHelpers.create(
            source=source,
            destination=destination,
            amount=amount,
            authorised_by=request.user,
            transaction_type=transaction_type
        )

        return resp.to_response()
