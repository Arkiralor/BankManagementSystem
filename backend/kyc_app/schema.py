from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from kyc_app.serializers import CustomerSerializer, KnowYourCustomerInputSerializer, KnowYourCustomerOutputSerializer, \
    KYCDocumentsInputSerializer, KYCDocumentsOutputSerializer, CustomerAddressInputSerializer, \
    CustomerAddressOutputSerializer

class CustomerCreateRequestSerializer(Serializer):
    customer = CustomerSerializer()
    kyc = KnowYourCustomerInputSerializer()
    kyc_documents = KYCDocumentsInputSerializer()
    address = CustomerAddressInputSerializer()

