from django.urls import path

from banking_app.apis import BankAccountAPI

URL_PREFIX = 'api/banking/'

urlpatterns = [
    path('account/', BankAccountAPI.as_view(), name='bank-account-api'),
]