from django.urls import path

from kyc_app.apis import CustomerAPI

URL_PREFIX = 'api/kyc/'

urlpatterns = [
    path('customer/', CustomerAPI.as_view(), name='customer-api'),
]