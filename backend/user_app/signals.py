from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from user_app.models import User, UserProfile, Address
from user_app.serializers import ShowUserSerializer
from user_app.utils import UserModelUtils

from user_app import logger


class UserSignalReciever:
    model = User

    @classmethod
    def created(cls, sender, instance, created, *args, **kwargs):
        if created:
            user_profile, _ = UserProfile.objects.get_or_create(user=instance)
            user_address, _ = Address.objects.get_or_create(user=instance)
            logger.info(f"User: {instance.email} created.")

    @classmethod
    def updated(cls, sender, instance, created, *args, **kwargs):
        if not created:
            logger.info(f"User: '{instance.email}' updated.")

    @classmethod
    def pre_delete(cls, sender, instance, *args, **kwargs):
        _ = UserModelUtils.insert_deleted_user_into_mongo(
            data=ShowUserSerializer(instance=instance).data)

    @classmethod
    def post_delete(cls, sender, instance, *args, **kwargs):
        _ = instance.id_proof.delete(save=False)
        _ = instance.address_proof.delete(save=False)


post_save.connect(receiver=UserSignalReciever.created,
                  sender=UserSignalReciever.model)
post_save.connect(receiver=UserSignalReciever.updated,
                  sender=UserSignalReciever.model)
pre_delete.connect(receiver=UserSignalReciever.pre_delete,
                   sender=UserSignalReciever.model)
post_delete.connect(receiver=UserSignalReciever.post_delete,
                    sender=UserSignalReciever.model)


class UserProfileSignalReciever:
    model = UserProfile

    @classmethod
    def created(cls, sender, instance, created, *args, **kwargs):
        if created:
            logger.info(f"Profile for user: '{instance.user.email}' created.")

    @classmethod
    def updated(cls, sender, instance, created, *args, **kwargs):
        if not created:
            logger.info(f"Profile for user: '{instance.user.email}' updated.")


post_save.connect(receiver=UserProfileSignalReciever.created,
                  sender=UserProfileSignalReciever.model)
post_save.connect(receiver=UserProfileSignalReciever.updated,
                  sender=UserProfileSignalReciever.model)
