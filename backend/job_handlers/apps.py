from django.apps import AppConfig


class JobHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_handlers'
    verbose_name = "Job Handlers"

    def ready(self):
        import job_handlers.signals