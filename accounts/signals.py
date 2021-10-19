from django.dispatch import receiver
from django.db.models.signals import post_init, post_save
from .models import Expert
from utils.images import crop_image, make_tmb


@receiver(post_init, sender=Expert)
def backup_image_path(instance, **kwargs):
    instance._current_avatar = instance.avatar

@receiver(post_save, sender=Expert)
def expert_post_save(instance, **kwargs):
    crop_image(instance.avatar.path, 255, 355)
    make_tmb(instance.avatar.path)
    if instance._current_avatar != instance.avatar:
        storage = instance._current_avatar.storage
        if storage.exists(instance._current_avatar.name):
            storage.delete(instance._current_avatar.name)
