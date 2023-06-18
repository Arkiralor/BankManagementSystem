from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from auth.permissions import IsAccountantOrTeller
from ledger_app.helpers import EmployeeLedgerAPIHelper

from ledger_app import logger


class EmployeeLedgerAPI(APIView):
    permission_classes = (IsAccountantOrTeller | IsAdminUser, )

    def get(self, request: Request, *args, **kwargs) -> Response:
        _id = request.query_params.get("id", None)
        user_id = request.query_params.get("user")
        if not user_id or user_id == "":
            user_id = f"{request.user.id}"
        from_date = request.query_params.get("from", None)
        to_date = request.query_params.get("to", None)

        resp = EmployeeLedgerAPIHelper.retrieve(
            _id = _id,
            user_id = user_id,
            from_date = from_date,
            to_date = to_date,
        )

        return resp.to_response()
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        resp = EmployeeLedgerAPIHelper.create(
            data=request.data,
            user=request.user
        )

        return resp.to_response()
    
    def put(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        _id = request.query_params.get("id", None)

        resp = EmployeeLedgerAPIHelper.update(
            _id=_id,
            data=data,
            user=request.user
        )

        return resp.to_response()