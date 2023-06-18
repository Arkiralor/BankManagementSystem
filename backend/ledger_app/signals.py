from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from ledger_app.models import EmployeeLedger

from ledger_app import logger


class EmployeeLedgerSignalReciever:

    model = EmployeeLedger

    @classmethod
    def post_save(cls, sender, instance:EmployeeLedger, created, **kwargs):
        if created:
            logger.info(f"New ledger entry created for {instance.employee} for {instance.created.date()}")

        else:
            logger.info(f"Ledger entry {instance.id} updated for {instance.employee}")

    
post_save.connect(receiver=EmployeeLedgerSignalReciever.post_save, sender=EmployeeLedgerSignalReciever.model)