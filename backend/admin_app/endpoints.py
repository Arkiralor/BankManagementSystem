from django.urls import path

from admin_app.apis import RequestLogsAPI, GetEnvironmentAPI, GetSystemInfo

PREFIX = "api/admin/"

urlpatterns = [
    path('system/', GetSystemInfo.as_view(), name='get-system-info'),
    path('env/', GetEnvironmentAPI.as_view(), name='get-environment'),
    path('logs/request/', RequestLogsAPI.as_view(), name='request-logs')
]