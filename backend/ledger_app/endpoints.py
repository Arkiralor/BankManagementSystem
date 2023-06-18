from django.urls import path

from ledger_app.apis import EmployeeLedgerAPI


URL_PREFIX = "api/ledger/"

urlpatterns = [
    path("entry/", EmployeeLedgerAPI.as_view(), name="ledger_entry"),
]