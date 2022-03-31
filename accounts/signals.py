import email
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init, post_save, pre_save
from .models import Expert, TeamMember, User, Customer
from utils.images import delete_image, get_tmb_path, image_processing
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
def expert_post_save(instance, created, **kwargs):
    image_processing(instance.avatar, instance._current_avatar, 255, 355, 200, 200)
    teammember, created = TeamMember.objects.get_or_create(expert=instance, is_expert=True)
    teammember.first_name = instance.first_name
    teammember.last_name = instance.last_name
    teammember.email = instance.email
    teammember.avatar = instance.avatar
    teammember.languages.set(objs=instance.languages.all())
    teammember.about = instance.about
    teammember.save()

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
    if not instance.is_expert:
        delete_image(instance._current_avatar)

@receiver(post_init, sender=Customer)
def team_member_post_init(instance, **kwargs):
    instance._current_avatar = instance.avatar

@receiver(post_save, sender=Customer)
def team_member_post_save(instance, **kwargs):
    image_processing(instance.avatar, instance._current_avatar, 255, 355, 200, 200)

@receiver(post_delete, sender=Customer)
def team_member_post_delete(instance, **kwargs):
    delete_image(instance._current_avatar)
