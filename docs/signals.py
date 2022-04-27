



from docs.models import LegalDocument
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from unidecode import unidecode


@receiver(pre_save, sender=LegalDocument)
def tour_type_pre_save(instance, sender, **kwargs):
    instance.docs_slug = slugify(unidecode(instance.name))