from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init, post_save
from .models import Expert, TeamMember, User
from utils.images import delete_image, image_processing
from traveler.settings import BASE_DIR
        

@receiver(post_init, sender=User)
def user_post_init(instance, **kwargs):
    instance._current_avatar = instance.avatar

@receiver(post_save, sender=User)
def user_post_save(instance, **kwargs):
    image_processing(instance.avatar, instance._current_avatar, 255, 355, 200, 200)

@receiver(post_delete, sender=User)
def user_post_delete(instance, **kwargs):
    delete_image(instance._current_avatar)

@receiver(post_init, sender=Expert)
def expert_post_init(instance, **kwargs):
    instance._current_avatar = instance.avatar

@receiver(post_save, sender=Expert)
def expert_post_save(instance, **kwargs):
    image_processing(instance.avatar, instance._current_avatar, 255, 355, 200, 200)

@receiver(post_delete, sender=Expert)
def expert_post_delete(instance, **kwargs):
    delete_image(instance._current_avatar)

@receiver(post_init, sender=TeamMember)
def team_member_post_init(instance, **kwargs):
    instance._current_avatar = instance.avatar

@receiver(post_save, sender=TeamMember)
def team_member_post_save(instance, **kwargs):
    image_processing(instance.avatar, instance._current_avatar, 255, 355, 200, 200)

@receiver(post_delete, sender=TeamMember)
def team_member_post_delete(instance, **kwargs):
    delete_image(instance._current_avatar)