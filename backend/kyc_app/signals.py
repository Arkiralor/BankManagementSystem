"""
Module to store signals and recievers used in the `kyc_app`.
"""

from PIL import Image

from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from kyc_app.models import KYCDocuments
from kyc_app import logger


class KycDocumentsReciever:
    """
    Class to handle the signals for KYCDocuments model.
    """

    model = KYCDocuments
    MAX_IMAGE_SIZE: int = 2_048
    QUALITY: int = 75
    OPTIMIZE: bool = True

    @classmethod
    def post_save(cls, sender, instance: KYCDocuments, created, *args, **kwargs):
        """
        POST-SAVE signal for KYCDocuments model.
        """
        if created:
            logger.info(
                f"KYC Documents for customer {instance.customer.id} created.")

    @classmethod
    def post_delete(cls, instance: KYCDocuments, sender, *args, **kwargs):
        """
        POST-DELETE signal for KYCDocuments model.

        Primarilly used to delete the files from the storage.
        """
        _ = instance.photo.delete(save=False)
        _ = instance.id_proof.delete(save=False)
        _ = instance.address_proof.delete(save=False)


post_save.connect(receiver=KycDocumentsReciever.post_save,
                  sender=KycDocumentsReciever.model)
post_delete.connect(receiver=KycDocumentsReciever.post_delete,
                    sender=KycDocumentsReciever.model)
