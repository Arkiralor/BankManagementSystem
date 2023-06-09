from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet, Count, Case, When, Value, IntegerField

from rest_framework import status
from rest_framework.parsers import FileUploadParser

from core.boilerplate.response_template import Resp
from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress
from kyc_app.serializers import CustomerSerializer, KnowYourCustomerInputSerializer, KnowYourCustomerOutputSerializer, \
    KYCDocumentsInputSerializer, KYCDocumentsOutputSerializer, CustomerAddressInputSerializer, \
    CustomerAddressOutputSerializer

from kyc_app import logger


class CustomerAPIHelper:

    ITEMS_PER_PAGE: int = settings.MAX_ITEMS_PER_PAGE

    @classmethod
    def search(cls, query: str = None, page: int = 1):
        """
        Method to search for customers based on their first name, last name, email, phone number or middle name.
        """
        resp = Resp()

        if not query or query == "":
            resp.error = "Invalid Search Query"
            resp.message = f"Query: {query}"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        customers = Customer.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(middle_name__icontains=query)
        ).distinct().annotate(
            relevance=Count(
                Case(
                    When(first_name__icontains=query, then=Value(1)),
                    When(last_name__icontains=query, then=Value(1)),
                    When(middle_name__icontains=query, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        ).order_by("-relevance", "-created")
        paginated = Paginator(customers, cls.ITEMS_PER_PAGE)
        customers = paginated.get_page(page)

        serialized = CustomerSerializer(customers, many=True).data

        resp.message = "Customers Retrieved Successfully"
        resp.data = {
            "totalPages": paginated.num_pages,
            "currentPage": page,
            "hits": paginated.count,
            "results": serialized
        }
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp

    @classmethod
    def get(cls, customer_id: str = None):
        return Customer.objects.filter(pk=customer_id).first()

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
    def get(cls, customer_id: str = None):
        kyc_documents = KYCDocuments.objects.filter(
            customer__id=customer_id).first()
        if not kyc_documents:
            logger.warn("Invalid Customer ID")
            raise ValueError("Invalid Customer ID")

        return kyc_documents

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

    @classmethod
    def add_documents(
        cls,
        customer_id: str = None,
        id_proof: TemporaryUploadedFile = None,
        address_proof: TemporaryUploadedFile = None,
        photo: TemporaryUploadedFile = None,
        *args,
        **kwargs
    ) -> Resp:
        resp = Resp()

        kyc_documents = cls.get(customer_id=customer_id)
        try:
            if id_proof:
                if kyc_documents.id_proof:
                    _ = kyc_documents.id_proof.delete(save=False)
                kyc_documents.id_proof = id_proof
            if address_proof:
                if kyc_documents.address_proof:
                    _ = kyc_documents.address_proof.delete(save=False)
                kyc_documents.address_proof = address_proof
            if photo:
                if kyc_documents.photo:
                    _ = kyc_documents.photo.delete(save=False)
                kyc_documents.photo = photo

            kyc_documents.save()
        except Exception as ex:
            resp.error = "Error while adding documents"
            resp.message = f"{ex}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.warn(resp.to_text())
            return resp

        resp.message = f"KYC documents successfully updated for customer<{customer_id}>."
        resp.data = KYCDocumentsOutputSerializer(kyc_documents).data
        resp.status_code = status.HTTP_200_OK

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
