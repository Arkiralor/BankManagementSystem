from django.apps import AppConfig


class AnalyticsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics_app'
    verbose_name = 'Analytics App'

    def ready(self):
        import analytics_app.signals
