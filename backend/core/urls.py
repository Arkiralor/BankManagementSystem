from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView

from core import logger

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/admin/', include('admin_app.endpoints')),
    path('api/analytics/', include('analytics_app.endpoints')),
    path('api/banking/', include('banking_app.endpoints')),
    path('api/kyc/', include('kyc_app.endpoints')),
    path('api/ledger/', include('ledger_app.endpoints')),
    path('api/user/', include('user_app.endpoints')),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/images/favicon.ico'))),
]

if settings.DEBUG and settings.ENV_TYPE.lower() == 'dev':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns.append(path('api/experiment/', include('experiments_app.endpoints')))


logger.info(f"Running in {settings.ENV_TYPE.upper()} mode with DEBUG: {settings.DEBUG}")