from django.urls import path

from analytics_app.apis import CustomerAnalyticsAPI

URL_PREFIX = 'api/analytics/'

urlpatterns = [
    # path('endpoint/', api.as_view(), name='api-name'),
    path('customers/', CustomerAnalyticsAPI.as_view(), name='customer-analytics-api'),
]