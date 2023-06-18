from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from auth.permissions import IsAccountantOrTeller
from analytics_app.helpers import CustomerAnalyticsHelper
from core.boilerplate.response_template import Resp

class CustomerAnalyticsAPI(APIView):
    permission_classes = (IsAccountantOrTeller | IsAdminUser,)

    def get(self, request: Request, *args, **kwargs):
        criteria = request.query_params.get("criteria")

        if criteria == "ageGroup":
            resp = CustomerAnalyticsHelper.get_customer_age_groups()
        elif criteria == "gender":
            resp = CustomerAnalyticsHelper.get_customers_by_gender()

        else:
            resp = Resp(
                error="error",
                message="Invalid criteria",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return resp.to_response()
