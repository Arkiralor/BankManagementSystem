from rest_framework import status

from core.boilerplate.response_template import Resp
from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress
from kyc_app.serializers import CustomerSerializer, KnowYourCustomerInputSerializer, KnowYourCustomerOutputSerializer, \
    KYCDocumentsInputSerializer, KYCDocumentsOutputSerializer, CustomerAddressInputSerializer, \
    CustomerAddressOutputSerializer

from kyc_app import logger


class CustomerAPIHelper:

    @classmethod
    def retrieve(cls, customer_id: str = None):
        resp = Resp()
        customer = Customer.objects.filter(pk=customer_id).first()
        if not customer:
            resp.error = "Customer Not Found"
            resp.message = f"Customer ID: {customer_id}"
            resp.status_code = status.HTTP_404_NOT_FOUND

            logger.warn(resp.message)
            return resp

        cust_serialized = CustomerSerializer(customer).data

        kyc = KnowYourCustomer.objects.filter(customer=customer).first()
        kyc_serialized = KnowYourCustomerOutputSerializer(
            kyc).data if kyc else {}
        kyc_documents = KYCDocuments.objects.filter(customer=customer).first()
        kyc_documents_serialized = KYCDocumentsOutputSerializer(
            kyc_documents).data if kyc_documents else {}
        address = CustomerAddress.objects.filter(customer=customer).first()
        address_serialized = CustomerAddressOutputSerializer(
            address).data if address else {}

        resp.message = "Customer Retrieved Successfully"
        resp.data = {
            "customer": cust_serialized,
            "kyc": kyc_serialized,
            "kyc_documents": kyc_documents_serialized,
            "address": address_serialized,
        }
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp

    @classmethod
    def create(cls, data: dict = None):
        resp = Resp()

        customer_data = data.get('customer', {})
        kyc_data = data.get('kyc', {})
        kyc_documents_data = data.get('kyc_documents', {})
        address_data = data.get('address', {})

        customer_serializer = CustomerSerializer(data=customer_data)
        if not customer_serializer.is_valid():
            resp.error = "Invalid Customer Data"
            resp.message = f"{customer_serializer.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        customer_serializer.save()
        customer: Customer = customer_serializer.instance

        kyc_created = KYCAPIHelper.create(data=kyc_data, customer=customer)
        if kyc_created.error:
            customer.delete()
            return kyc_created

        kyc_documents_created = KYCDocumentsAPIHelper.create(
            data=kyc_documents_data, customer=customer)
        if kyc_documents_created.error:
            customer.delete()
            return kyc_documents_created

        address_created = CustomerAddressAPIHelper.create(
            data=address_data, customer=customer)
        if address_created.error:
            customer.delete()
            return address_created

        resp.message = "Customer Created Successfully"
        resp.data = {
            "customer": customer_serializer.data,
            "kyc": kyc_created.data.get('data'),
            "kyc_documents": kyc_documents_created.data.get('data'),
            "address": address_created.data.get('data'),
        }
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp


class KYCAPIHelper:

    @classmethod
    def create(cls, data: dict = None, customer: Customer = None):
        resp = Resp()

        if not customer or not isinstance(customer, Customer) or not data:
            resp.error = "Invalid Customer Data"
            resp.message = f"Customer: {customer} | Data: {data}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        data["customer"] = f"{customer.id}"

        deserialized = KnowYourCustomerInputSerializer(data=data)
        if not deserialized.is_valid():
            resp.error = "Invalid KYC Data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        deserialized.save()
        kyc: KnowYourCustomer = deserialized.instance

        resp.message = "KYC Created Successfully"
        resp.data = {
            "data": deserialized.data,
            "instance": kyc
        }
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp


class KYCDocumentsAPIHelper:

    @classmethod
    def create(cls, data: dict = None, customer: Customer = None):
        resp = Resp()

        if not customer or not isinstance(customer, Customer) or not data:
            resp.error = "Invalid Customer Data"
            resp.message = f"Customer: {customer} | Data: {data}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        data["customer"] = f"{customer.id}"

        deserialized = KYCDocumentsInputSerializer(data=data)
        if not deserialized.is_valid():
            resp.error = "Invalid KYC Documents Data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        deserialized.save()
        kyc_documents: KYCDocuments = deserialized.instance

        resp.message = "KYC Documents Created Successfully"
        resp.data = {
            "data": deserialized.data,
            "instance": kyc_documents
        }
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp


class CustomerAddressAPIHelper:

    @classmethod
    def create(cls, data: dict = None, customer: Customer = None):
        resp = Resp()

        if not customer or not isinstance(customer, Customer) or not data:
            resp.error = "Invalid Customer Data"
            resp.message = f"Customer: {customer} | Data: {data}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        data["customer"] = f"{customer.id}"

        deserialized = CustomerAddressInputSerializer(data=data)
        if not deserialized.is_valid():
            resp.error = "Invalid Customer Address Data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        deserialized.save()
        customer_address: CustomerAddress = deserialized.instance

        resp.message = "Customer Address Created Successfully"
        resp.data = {
            "data": deserialized.data,
            "instance": customer_address
        }
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp
