DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken'
]

CUSTOM_APPS = [
    'admin_app.apps.AdminAppConfig',
    'communications_app.apps.CommunicationsAppConfig',
    'middleware_app.apps.MiddlewareAppConfig',
    'banking_app.apps.BankingAppConfig',
    'kyc_app.apps.KycAppConfig',
    'user_app.apps.UserAppConfig'
]