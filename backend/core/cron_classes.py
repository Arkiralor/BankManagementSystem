JOB_HANDLER_CLASSES = [
    'job_handlers.cron.MonitorEnqueuedJob',
    'job_handlers.cron.DeleteOldJobRecords'
]

USER_APP_CLASSES = [
    'user_app.cron.RemoveInactiveUser'
]