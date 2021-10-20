from django.dispatch import receiver
from django.db.models.signals import post_init, post_save
from .models import Expert, User
from utils.images import crop_image, make_tmb
import os
from traveler.settings import BASE_DIR

def avatar_processing(instance):
    crop_image(instance.avatar.path, 255, 355)
    make_tmb(instance.avatar.path)
    if instance._current_avatar != instance.avatar:
        storage = instance._current_avatar.storage
        if storage.exists(instance._current_avatar.name):
            storage.delete(instance._current_avatar.name)
        if os.path.exists(f'{BASE_DIR}{instance._current_tmb_avatar}'):
            os.remove(f'{BASE_DIR}{instance._current_tmb_avatar}')


@receiver(post_init, sender=User)
def backup_image_path(instance, **kwargs):
    instance._current_avatar = instance.avatar
    instance._current_tmb_avatar = instance.tmb_avatar

@receiver(post_save, sender=User)
def expert_post_save(instance, **kwargs):
    avatar_processing(instance)

@receiver(post_init, sender=Expert)
def backup_image_path(instance, **kwargs):
    instance._current_avatar = instance.avatar
    instance._current_tmb_avatar = instance.tmb_avatar

@receiver(post_save, sender=Expert)
def expert_post_save(instance, **kwargs):
    avatar_processing(instance)
