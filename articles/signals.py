from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.template.defaultfilters import slugify
from unidecode import unidecode
from utils.images import delete_image, image_processing, get_current_img
from .models import Article, Blog
import math


@receiver(pre_save, sender=Article)
def article_pre_save(instance, **kwargs):
    instance.slug = slugify(unidecode(instance.title))
    imgs = instance.text.count('<img')
    instance.reading_time = math.ceil((len(instance.text)/1500)+0.2*imgs)

@receiver(post_save, sender=Article)
def articlc_post_save(instance, created, **kwargs):
    if instance.image:
        image_processing(instance.image, None, 1920, 480, 730, 417)

@receiver(pre_save, sender=Blog)
def blog_pre_save(instance, **kwargs):
    instance.slug = slugify(unidecode(instance.title))

@receiver(post_save, sender=Blog)
def blog_post_save(instance, created, **kwargs):
    if instance.image:
        image_processing(instance.image, None, 1920, 480, 730, 417)