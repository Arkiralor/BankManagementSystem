from datetime import datetime, date, timedelta

from rest_framework import status

from django.db.models import Q, QuerySet, Count, When, Value, Case, Func
from django.utils import timezone

from analytics_app.utils import CustomerAnalyticsUtils, TransactionAnalyticsUtils
from core.boilerplate.response_template import Resp
from banking_app.models import Account, Transaction
from banking_app.model_choices import AccountChoice, TransactionChoice
from banking_app.serializers import AccountInputSerializer, AccountOutputSerializer, TransactionInputSerializer, TransactionOutputSerializer
from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress
from kyc_app.model_choices import CustomerChoice
from kyc_app.serializers import CustomerSerializer, KnowYourCustomerInputSerializer, KnowYourCustomerOutputSerializer, KYCDocumentsInputSerializer,\
    KYCDocumentsOutputSerializer, CustomerAddressInputSerializer, CustomerAddressOutputSerializer

from analytics_app import logger

class CustomerAnalyticsHelper:

    @classmethod
    def get_customer_age_groups(cls):
        resp = Resp()

        customers = CustomerAnalyticsUtils.get_customer_age_groups()
        if not customers:
            resp.error = "Server Error"
            resp.message = "Error fetching customer age groups"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.info(resp.to_text())
            return resp
        
        resp.message = "Customer age groups fetched successfully"
        resp.data = customers
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp
    
    @classmethod
    def get_customers_by_gender(cls):
        resp = Resp()

        customers = CustomerAnalyticsUtils.get_customers_by_gender()
        if not customers:
            resp.error = "Server Error"
            resp.message = "Error fetching customer gender groups."
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.warn(resp.to_text())
            return resp
        
        resp.message = "Customer gender groups fetched successfully"
        resp.data = customers
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp


class TransactionAnalyticsHelper:

    @classmethod
    def get_txn_by_type(cls):
        resp = Resp()

        txn_data = TransactionAnalyticsUtils.get_transactions_by_type()

        if not txn_data:
            resp.error = "Server Error"
            resp.message = "Error fetching transaction data"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.warn(resp.to_text())
            return resp

        resp.message = "Transaction data fetched successfully"
        resp.data = txn_data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp

    @classmethod
    def get_txn_by_amount(cls):
        resp = Resp()

        txn_data = TransactionAnalyticsUtils.get_transaction_by_amount() 

        if not txn_data:
            resp.error = "Server Error"
            resp.message = "Error fetching transaction data"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.warn(resp.to_text())
            return resp

        resp.message = "Transaction data fetched successfully"
        resp.data = txn_data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp    
    
    @classmethod
    def get_txn_by_date(cls):
        resp = Resp()

        txn_data = TransactionAnalyticsUtils.get_transactions_by_date() 

        if not txn_data:
            resp.error = "Server Error"
            resp.message = "Error fetching transaction data"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.warn(resp.to_text())
            return resp

        resp.message = "Transaction data fetched successfully"
        resp.data = txn_data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp