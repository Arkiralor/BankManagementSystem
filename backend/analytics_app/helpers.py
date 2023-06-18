from datetime import datetime, date, timedelta

from rest_framework import status

from django.db.models import Q, QuerySet, Count, When, Value, Case, Func
from django.db.models.functions import ExtractYear
from django.utils import timezone

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

        try:
            customers = Customer.objects.all().annotate(
                age=Case(
                    When(date_of_birth__isnull=True, then=Value(0)),
                    default=timezone.now().year - ExtractYear("date_of_birth")
                )
            ).annotate(
                age_group=Case(
                    When(age__gte=0, age__lte=17, then=Value("0-17")),
                    When(age__gte=18, age__lte=25, then=Value("18-25")),
                    When(age__gte=26, age__lte=35, then=Value("26-35")),
                    When(age__gte=36, age__lte=45, then=Value("36-45")),
                    When(age__gte=46, age__lte=55, then=Value("46-55")),
                    When(age__gte=56, age__lte=65, then=Value("56-65")),
                    When(age__gte=66, age__lte=75, then=Value("66-75")),
                    When(age__gte=76, age__lte=85, then=Value("76-85")),
                    When(age__gte=86, then=Value("86+")),
                    default=Value("Unknown")
                )
            ).values("age_group").annotate(count=Count("age_group")).order_by("age_group")
        except Exception as ex:
            resp.error = "error"
            resp.message = f"Error fetching customer age groups: {ex}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return resp



        resp.message = "Customer age groups fetched successfully"
        resp.data = customers
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp
    
    @classmethod
    def get_customers_by_gender(cls):
        resp = Resp()

        try:
            customers = Customer.objects.all().annotate(
                group=Case(
                    When(gender__isnull=True, then=Value("Unknown")),
                    When(gender=CustomerChoice.female, then=Value("Female")),
                    When(gender=CustomerChoice.male, then=Value("Male")),
                    When(gender=CustomerChoice.other, then=Value("Other"))
                )
            ).values("group").annotate(count=Count("group")).order_by("group")
        except Exception as ex:
            resp.error = "error"
            resp.message = f"Error fetching customer gender groups: {ex}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return resp
        
        resp.message = "Customer gender groups fetched successfully"
        resp.data = customers
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp


        