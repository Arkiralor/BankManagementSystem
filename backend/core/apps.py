DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'django_rq',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rq',
    'storages'
]

CUSTOM_APPS = [
    'admin_app.apps.AdminAppConfig',
    'analytics_app.apps.AnalyticsAppConfig',
    'banking_app.apps.BankingAppConfig',
    'communications_app.apps.CommunicationsAppConfig',
    'experiments_app.apps.ExperimentsAppConfig',
    'kyc_app.apps.KycAppConfig',
    'ledger_app.apps.LedgerAppConfig',
    'management_app.apps.ManagementAppConfig',
    'middleware_app.apps.MiddlewareAppConfig',
    'user_app.apps.UserAppConfig'
]