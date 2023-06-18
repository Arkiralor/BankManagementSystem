from rest_framework.serializers import ModelSerializer

from ledger_app.models import EmployeeLedger
from user_app.serializers import ShowUserSerializer

from ledger_app import logger


class EmployeeLedgerInputSerializer(ModelSerializer):
    class Meta:
        model = EmployeeLedger
        fields = '__all__'


class EmployeeLedgerOutputSerializer(ModelSerializer):
    employee = ShowUserSerializer()

    class Meta:
        model = EmployeeLedger
        fields = '__all__'
