from django.urls import path

from admin_app.apis import RequestLogsAPI, GetEnvironmentAPI

PREFIX = "api/admin/"

urlpatterns = [
    path('env/', GetEnvironmentAPI.as_view(), name='get-environment'),
    path('logs/request/', RequestLogsAPI.as_view(), name='request-logs')
]