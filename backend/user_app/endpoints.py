from django.urls import path

from user_app.apis import AccessTestAPI, RegisterUserAPI, PasswordLoginAPI, UserAPI, WhiteListIpAddressAPI, \
    UserProfileAPI

PREFIX = "api/user/"

urlpatterns = [
    path('auth-test/', AccessTestAPI.as_view(), name='test-auth'),
    path('info/', UserAPI.as_view(), name='user-api'),
    path('login/password/', PasswordLoginAPI.as_view(), name='password-login'),
    path('signup/', RegisterUserAPI.as_view(), name='signup'),
    path('whitelist-ip/', WhiteListIpAddressAPI.as_view(), name='ip-whitelist-user'),
    path('profile/', UserProfileAPI.as_view(), name='profile-api'),
]