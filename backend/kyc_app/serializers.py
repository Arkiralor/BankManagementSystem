from rest_framework.serializers import ModelSerializer

from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class KnowYourCustomerInputSerializer(ModelSerializer):

    class Meta:
        model = KnowYourCustomer
        fields = '__all__'


class KnowYourCustomerOutputSerializer(ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = KnowYourCustomer
        fields = '__all__'


class KYCDocumentsInputSerializer(ModelSerializer):

    class Meta:
        model = KYCDocuments
        fields = '__all__'


class KYCDocumentsOutputSerializer(ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = KYCDocuments
        fields = '__all__'


class CustomerAddressInputSerializer(ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = '__all__'


class CustomerAddressOutputSerializer(ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = CustomerAddress
        fields = '__all__'
