from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from accounts.models import Expert
from tours.models import TourBasic, TourDay, TourDayImage, TourImage, TourPropertyImage, TourType
from utils.images import delete_image, image_processing
from django.db.models import Count, Q
        

@receiver(pre_save, sender=TourType)
def tour_type_pre_save(instance, **kwargs):
    try:
        instance._current_img = TourType.objects.get(pk=instance.id).wallpaper
    except:
        instance._current_img = ''

@receiver(post_save, sender=TourType)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)

@receiver(post_delete, sender=TourType)
def tour_type_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(pre_save, sender=TourBasic)
def tour_basic_pre_save(instance, **kwargs):
    try:
        current_tour_basic = TourBasic.objects.get(pk=instance.id)
        instance._current_img = current_tour_basic.wallpaper
        if current_tour_basic.is_active:
            instance.is_active = False
            instance.on_moderation = True
    except:
        instance._current_img = ''

@receiver(post_save, sender=TourBasic)
def tour_basic_post_save(instance, created, **kwargs):
    image_processing(instance.wallpaper, instance._current_img, 1920, 480, 730, 280)
    expert = instance.expert
    expert.tours_count = Expert.objects.filter(pk=expert.id).aggregate(count=Count('tours', filter=Q(tours__is_active=True)))['count']
    expert.save()

@receiver(post_delete, sender=TourBasic)
def tour_basic_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(pre_save, sender=TourPropertyImage)
def tour_property_image_pre_save(instance, **kwargs):
    try:
        instance._current_img = TourPropertyImage.objects.get(pk=instance.id).wallpaper
    except:
        instance._current_img = ''

@receiver(post_save, sender=TourPropertyImage)
def tour_property_image_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 1067, 800, 350, 240, True)

@receiver(post_delete, sender=TourPropertyImage)
def tour_property_image_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(pre_save, sender=TourImage)
def tour_image_pre_save(instance, **kwargs):
    try:
        instance._current_img = TourImage.objects.get(pk=instance.id).wallpaper
    except:
        instance._current_img = ''

@receiver(post_save, sender=TourImage)
def tour_image_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 1067, 800, 350, 240, True)

@receiver(post_delete, sender=TourImage)
def tour_image_post_delete(instance, **kwargs):
    delete_image(instance._current_img)

@receiver(pre_save, sender=TourDay)
def tour_day_image_pre_save(instance, **kwargs):
    try:
        instance._current_img = TourDay.objects.get(pk=instance.id).image
    except:
        instance._current_img = ''

@receiver(post_save, sender=TourDay)
def tour_day_image_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 730, 400)

@receiver(post_delete, sender=TourDay)
def tour_day_image_post_delete(instance, **kwargs):
    delete_image(instance._current_img)