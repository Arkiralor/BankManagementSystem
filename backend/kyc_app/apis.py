from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from auth.permissions import IsAccountantOrTeller
from core.boilerplate.request_template import validate_request_body
from kyc_app.helpers import CustomerAPIHelper, KYCDocumentsAPIHelper
from kyc_app.schema import CustomerCreateRequestSerializer


class CustomerAPI(APIView):
    permission_classes = (IsAccountantOrTeller,)

    def get(self, request: Request, *args, **kwargs):

        customer_id = request.query_params.get('customer')
        resp = CustomerAPIHelper.retrieve(customer_id=customer_id)
        return resp.to_response()

    def post(self, request: Request, *args, **kwargs):
        data = request.data

        resp = CustomerAPIHelper.create(data=data)
        return resp.to_response()

    def put(self, request: Request, *args, **kwargs):
        query = request.data.get('query')
        page = int(request.data.get('page', 1))
        resp = CustomerAPIHelper.search(query=query)
        return resp.to_response()


class KYCDocumentsAPI(APIView):
    permission_classes = (IsAccountantOrTeller, )

    ID_PROOF: str = "idProof"
    ADDRESS_PROOF: str = "addressProof"
    PHOTO: str = "photo"

    def put(self, request: Request, *args, **kwargs):

        customer_id = request.query_params.get("customer")
        id_proof = request.FILES.get(self.ID_PROOF)
        address_proof = request.FILES.get(self.ADDRESS_PROOF)
        photo = request.FILES.get(self.PHOTO)

        resp = KYCDocumentsAPIHelper.add_documents(
            customer_id=customer_id, id_proof=id_proof, address_proof=address_proof, photo=photo)
        return resp.to_response()
