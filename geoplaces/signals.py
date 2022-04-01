from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init, post_save
from geoplaces.models import City, Country, Region
from utils.images import delete_image, image_processing
        

@receiver(post_init, sender=Region)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=Region)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)

@receiver(post_delete, sender=Region)
def tour_type_post_delete(instance, **kwargs):
    if instance.image:
        delete_image(instance.image)

@receiver(post_init, sender=Country)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=Country)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)

@receiver(post_delete, sender=Country)
def tour_type_post_delete(instance, **kwargs):
    if instance.image:
        delete_image(instance.image)

@receiver(post_init, sender=City)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=City)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)
    # if instance.country:


@receiver(post_delete, sender=City)
def tour_type_post_delete(instance, **kwargs):
    if instance.image:
        delete_image(instance.image)