from django.apps import AppConfig


class KycAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kyc_app'
    verbose_name = "KYC App"

    def ready(self):
        import kyc_app.signals
