from PIL import Image
from io import BytesIO

from django.db.models import ImageField
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from kyc_app.models import KYCDocuments
from kyc_app import logger


class KycDocumentsReciever:
    model = KYCDocuments
    MAX_IMAGE_SIZE: int = 2_048
    QUALITY: int = 75
    OPTIMIZE: bool = True

    @classmethod
    def post_save(cls, sender, instance: KYCDocuments, created, *args, **kwargs):
        if created:
            if instance.photo:
                instance.photo.name = f"{instance.customer.id}-photo.{instance.photo.name.split('.')[-1]}"

                photo = Image.open(instance.photo.file)
                photo.save(instance.photo.file, quality=cls.QUALITY, optimize=cls.OPTIMIZE)

            if instance.id_proof:
                instance.id_proof.name = f"{instance.customer.id}-id.{instance.id_proof.name.split('.')[-1]}"

                id_proof = Image.open(instance.id_proof.file)
                id_proof.save(instance.id_proof.file,
                              quality=cls.QUALITY, optimize=cls.OPTIMIZE)
                
            if instance.address_proof:
                instance.address_proof.name = f"{instance.customer.id}-address.{instance.address_proof.name.split('.')[-1]}"

                address_proof = Image.open(instance.address_proof.file)
                address_proof.save(instance.address_proof.file,
                                   quality=cls.QUALITY, optimize=cls.OPTIMIZE)
            
            logger.info(f"KYC Documents for customer {instance.customer.id} created.")

    @classmethod
    def post_delete(cls, instance: KYCDocuments, sender, *args, **kwargs):
        _ = instance.photo.delete(save=False)
        _ = instance.id_proof.delete(save=False)
        _ = instance.address_proof.delete(save=False)


post_save.connect(receiver=KycDocumentsReciever.post_save,
                  sender=KycDocumentsReciever.model)
post_delete.connect(receiver=KycDocumentsReciever.post_delete,
                    sender=KycDocumentsReciever.model)
