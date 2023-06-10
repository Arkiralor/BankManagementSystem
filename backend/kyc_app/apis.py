from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from auth.permissions import IsAccountantOrTeller
from core.boilerplate.request_template import validate_request_body
from kyc_app.helpers import CustomerAPIHelper
from kyc_app.schema import CustomerCreateRequestSerializer


class CustomerAPI(APIView):
    permission_classes = (IsAccountantOrTeller,)

    def get(self, request:Request, *args, **kwargs):
        
        customer_id = request.data.get('customer')
        resp = CustomerAPIHelper.retrieve(customer_id=customer_id)
        return resp.to_response()

    def post(self, request:Request, *args, **kwargs):
        data = request.data
        if not validate_request_body(request_data=data, request_schema=CustomerCreateRequestSerializer):
            return Response(
                {
                    "error": "Invalid Request Body",
                    "message": "Please check the request body and try again."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resp = CustomerAPIHelper.create(data=data)
        return resp.to_response()
