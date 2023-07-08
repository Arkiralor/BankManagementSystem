from django_cron import CronJobBase, Schedule

from django.db.models import Q
from django.utils import timezone

from user_app.models import User


class RemoveInactiveUser(CronJobBase):
    RUN_AT_TIMES = ['00:00', '12:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'remove_old_inactive_users'

    def do(self):
        SEVEN_DAYS_AGO = timezone.now() - timezone.timedelta(days=7)
        old_users = User.objects.filter(
            Q(is_active=False)
            & Q(date_joined__lte=SEVEN_DAYS_AGO)
        ).delete()