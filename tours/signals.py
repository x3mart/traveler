from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init, post_save
from tours.models import TourBasic, TourDayImage, TourImage, TourPropertyImage, TourType
from utils.images import delete_image, image_processing
        

@receiver(post_init, sender=TourType)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=TourType)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)

@receiver(post_delete, sender=TourType)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(post_init, sender=TourBasic)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.wallpaper

@receiver(post_save, sender=TourBasic)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.wallpaper, instance._current_img, 1920, 480, 730, 280)

@receiver(post_delete, sender=TourBasic)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(post_init, sender=TourPropertyImage)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=TourPropertyImage)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 1067, 800, 350, 240, True)

@receiver(post_delete, sender=TourPropertyImage)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(post_init, sender=TourImage)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=TourImage)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 1067, 800, 350, 240, True)

@receiver(post_delete, sender=TourImage)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(post_init, sender=TourDayImage)
def tour_type_post_init(instance, **kwargs):
    instance._current_img = instance.image

@receiver(post_save, sender=TourDayImage)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 730, 400)

@receiver(post_delete, sender=TourDayImage)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)