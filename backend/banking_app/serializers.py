from rest_framework.serializers import ModelSerializer

from banking_app.models import Account, Transaction
from kyc_app.serializers import CustomerSerializer
from user_app.serializers import ShowUserSerializer


class AccountInputSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class AccountOutputSerializer(ModelSerializer):
    holder = CustomerSerializer(many=True)

    class Meta:
        model = Account
        fields = '__all__'


class TransactionInputSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionOutputSerializer(ModelSerializer):
    source = AccountInputSerializer()
    destination = AccountInputSerializer()
    authorised_by = ShowUserSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'
