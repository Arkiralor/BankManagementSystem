from django.contrib import admin

from job_handlers.models import EnqueuedJob

@admin.register(EnqueuedJob)
class EnqueuedJobAdmin(admin.ModelAdmin):
    list_display = ("id", "job_id", "_func_name", "_status", "origin", "created")
    search_fields = (
        "id",
        "job_id",
        "_func_name",
        "_status",
        "origin",
    )
    ordering = ("-created",)
    list_filter = ("_status", "origin")