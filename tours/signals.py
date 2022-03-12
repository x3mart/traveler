from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from accounts.models import Expert
from tours.models import Tour, TourBasic, TourDayImage, TourGuestGuideImage, TourImage, TourPlanImage, TourPropertyImage, TourType, TourWallpaper
from utils.images import delete_image, image_processing, get_current_img
from django.db.models import Count, Q
        

@receiver(pre_save, sender=TourType)
def tour_type_pre_save(instance, sender, **kwargs):
    instance._current_img = get_current_img(sender, instance)

@receiver(post_save, sender=TourType)
def tour_type_post_save(instance, **kwargs):
    image_processing(instance.image, instance._current_img, 350, 240)

@receiver(post_delete, sender=TourType)
def tour_type_post_delete(instance, **kwargs):
    if instance.image:
        delete_image(instance.image)


    if instance.discount == 0:
        instance.discount = None
    if instance.discount and instance.discount_in_prc:
        instance.cost = instance.price - instance.price*instance.discount/100
    elif instance.discount and not instance.discount_in_prc:
        instance.cost = instance.price - instance.discount
    else:
        instance.cost = instance.price
    if instance.finish_date and instance.start_date:
        instance.duration = (instance.finish_date - instance.start_date).days + 1

@receiver(post_save, sender=Tour)
def tour_post_save(instance, **kwargs):
    expert = instance.tour_basic.expert
    expert.tours_count = expert.tours.filter(tours__is_active=True).distinct().count()
    expert.save()

@receiver(post_save, sender=TourWallpaper)
def tour_basic_post_save(instance, created, **kwargs):
    image_processing(instance.wallpaper, None, 1920, 480, 730, 280)

    

# @receiver(post_delete, sender=Tour)
# def tour_basic_post_delete(instance, **kwargs):
#     if instance.wallpaper:
#         delete_image(instance.wallpaper)


@receiver(post_save, sender=TourBasic)
def tour_basic_post_save(instance, created, **kwargs):
    expert = instance.expert
    expert.tours_count = Expert.objects.filter(pk=expert.id).aggregate(count=Count('tours', filter=Q(tours__is_active=True)&Q(tours__direct_link=False)))['count']
    expert.save()
    

# @receiver(pre_save, sender=TourPropertyImage)
# def tour_property_image_pre_save(instance, sender, **kwargs):
#     instance._current_img = get_current_img(sender, instance)

@receiver(post_save, sender=TourPropertyImage)
def tour_property_image_post_save(instance, **kwargs):
    image_processing(instance.image, None, 1067, 800, 350, 240, True)

@receiver(post_delete, sender=TourPropertyImage)
def tour_property_image_post_delete(instance, **kwargs):
    if instance.image:
        delete_image(instance.image)

# @receiver(pre_save, sender=TourImage)
# def tour_image_pre_save(instance, sender, **kwargs):
#     instance._current_img = get_current_img(sender, instance)

@receiver(post_save, sender=TourImage)
def tour_image_post_save(instance, **kwargs):
    image_processing(instance.image, None, 1067, 800, 350, 240, True)

# @receiver(post_delete, sender=TourImage)
# def tour_image_post_delete(instance, **kwargs):
#     if instance.image:
#         delete_image(instance.image)

# @receiver(pre_save, sender=TourDayImage)
# def tour_day_image_pre_save(instance, sender, **kwargs):
#     instance._current_img = get_current_img(sender, instance)

@receiver(post_save, sender=TourDayImage)
def tour_day_image_post_save(instance, **kwargs):
    image_processing(instance.image, None, 730, 400, 365, 200, True)

@receiver(post_save, sender=TourPlanImage)
def tour_plan_image_post_save(instance, **kwargs):
    image_processing(instance.image, None, 730, 400, 365, 200)

# @receiver(post_delete, sender=TourDayImage)
# def tour_day_image_post_delete(instance, **kwargs):
#     if instance.image:
#         delete_image(instance.image)

@receiver(post_save, sender=TourGuestGuideImage)
def expert_post_save(instance, created, **kwargs):
    image_processing(instance.image, None, 255, 355, 200, 200)