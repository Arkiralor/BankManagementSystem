from django.db import models

from core.boilerplate.model_template import TemplateModel
from user_app.models import User


class EmployeeLedger(TemplateModel):
    employee = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.title if self.title else f"{self.body[:50:]}..."

    def __repr__(self) -> str:
        return self.__str__()
    
    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.strip().title()

        self.body = self.body.rstrip().lstrip()

        super(EmployeeLedger, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Employee Ledger'
        verbose_name_plural = 'Employee Ledgers'
        ordering = ('-created',)

        indexes = (
            models.Index(fields=('id',)),
            models.Index(fields=('employee',)),
            models.Index(fields=('title','body',)),
        )
