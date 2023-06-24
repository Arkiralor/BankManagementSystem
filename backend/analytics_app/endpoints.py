from django.urls import path

from analytics_app.apis import CustomerAnalyticsAPI, TransactionAnalyticsAPI

URL_PREFIX = 'api/analytics/'

urlpatterns = [
    # path('endpoint/', api.as_view(), name='api-name'),
    path('customers/', CustomerAnalyticsAPI.as_view(), name='customer-analytics-api'),
    path('transactions/', TransactionAnalyticsAPI.as_view(), name='transaction-analytics-api')
]