from os import environ

from django.conf import settings

from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from core.boilerplate.response_template import Resp
from user_app.serializers import ShowUserSerializer
from user_app.utils import UserModelUtils, UserProfileModelUtils

from user_app import logger


class GetEnvironmentAPI(APIView):
    """
    API to get environment variables.

    This API is only accessible by admin users in production/QA.
    """
    if settings.DEBUG:
        permission_classes = (IsAuthenticated | AllowAny,)
    else:
        permission_classes = (IsAdminUser,)

    def post(self, request: Request, *args, **kwargs):
        return Response(
            environ,
            status=status.HTTP_200_OK
        )


class AccessTestAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        resp = Resp(
            message="Access token working successfully.",
            data={
                "user": ShowUserSerializer(request.user).data,
                "message": "Access token working successfully."
            },
            status_code=status.HTTP_200_OK
        )

        logger.info(resp.message)

        return resp.to_response()

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        params = request.query_params
        user = request.user

        resp = Resp(
            message="Authentication successfull in POST method.",
            data={
                "body": data,
                "params": params,
                "user": ShowUserSerializer(user).data
            },
            status_code=status.HTTP_200_OK
        )

        return resp.to_response()


class RegisterUserAPI(APIView):
    """
    API to register a new user.
    """
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        user_type = request.query_params.get("type", "teller")

        resp = UserModelUtils.create(data=data, user_type=user_type)

        _ = UserModelUtils.log_login_ip(
            user=f"{resp.data.get('id', '')}", request=request)
        return resp.to_response()


class PasswordLoginAPI(APIView):
    """
    API to login a user via password.
    """
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        password = request.data.get("password", "")

        resp = UserModelUtils.login_via_password(
            username=username, email=email, password=password)

        _ = UserModelUtils.log_login_ip(
            user=f"{resp.data.get('user', '')}", request=request)
        _ = UserModelUtils.log_login_mac(
            user=f"{resp.data.get('user', '')}", request=request)
        return resp.to_response()


class UserAPI(APIView):
    """
    API to hold user information related functionality.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        """
        API to get a user's information.
        """
        user_id = request.query_params.get("user_id")
        if not user_id:
            user_id = request.user.id

        resp = UserModelUtils.get(user_id=user_id)

        return resp.to_response()

    def post(self, request: Request, page: int = 1, *args, **kwargs):
        """
        API to search for users.
        """
        term = request.query_params.get("term", "")
        page = int(request.query_params.get("page", 1))

        resp = UserModelUtils.search(term=term, page=page)

        return resp.to_response()

    def put(self, request: Request, *args, **kwargs):
        """
        API to let a user update their account information.
        """
        user_id = request.user.id
        data = request.data

        resp = UserProfileModelUtils.put(user_id=user_id, data=data)

        return resp.to_response()

    def delete(self, request: Request, *args, **kwargs):
        """
        API to let a user delete their account.
        """
        password = request.data.get("password")
        reason = request.data.get("reason", "No reason given.")
        resp = UserModelUtils.delete(
            user=request.user, password=password, reason=reason)

        return resp.to_response()


class WhiteListIpAddressAPI(APIView):
    """
    API for a user to set/get Whitelisted IP addresses.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        """
        Get all IP addresses whitelisted for user.
        """
        page = int(request.query_params.get("page", 1))
        resp = UserModelUtils.get_whitelisted_ips(user=request.user, page=page)

        return resp.to_response()

    def post(self, request: Request, *args, **kwargs):
        """
        Add IP addresses to whitelist for user.
        """
        password = request.data.get("password", None)
        ip_addresses = request.data.get("ip_addresses", [])

        if not type(ip_addresses) == list and not type(ip_addresses) == set:
            ip_addresses = [ip_addresses]

        resp = UserModelUtils.add_white_list_ips(
            user=request.user, password=password, ips=ip_addresses)

        return resp.to_response()

    def delete(self, request: Request, *args, **kwargs):
        """
        Delete a single whitelisted IP address for a user.
        """
        _id = request.data.get("id")
        ip = request.data.get("ip")

        resp = UserModelUtils.delete_whitelisted_ip(
            user=request.user, ip=ip, _id=_id)

        return resp.to_response()


class UserProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        """
        API to get a user's profile information.
        """
        user_id = request.query_params.get("user", f"{request.user.id}")

        resp = UserProfileModelUtils.retrieve(user_id=user_id)

        return resp.to_response()

    def put(self, request: Request, *args, **kwargs):
        """
        API to let a user update their profile information.
        """
        user_id = request.user.id
        data = request.data

        resp = UserProfileModelUtils.put(user_id=user_id, data=data)

        return resp.to_response()
