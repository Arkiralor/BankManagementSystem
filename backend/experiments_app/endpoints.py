from django.urls import path

from experiments_app.apis import TestEnqueue

URL_PREFIX = 'api/experiment/'

urlpatterns = [
    path('test-enqueue/', TestEnqueue.as_view(), name='test-enqueue'),
]