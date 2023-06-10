from django.apps import AppConfig


class BankingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banking_app'
    verbose_name = "Banking App"

    def ready(self):
        import banking_app.signals
