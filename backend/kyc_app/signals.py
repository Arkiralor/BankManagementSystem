from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from kyc_app.models import KYCDocuments

class KycDocumentsReciever:
    model = KYCDocuments

    @classmethod
    def post_delete(cls, instance, sender, *args, **kwargs):
        _ = instance.photo.delete(save=False)
        _ = instance.id_proof.delete(save=False)
        _ = instance.address_proof.delete(save=False)


post_delete.connect(receiver=KycDocumentsReciever.post_delete,
                    sender=KycDocumentsReciever.model)