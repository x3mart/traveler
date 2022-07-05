from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.apps import apps
from geoplaces.models import City, Country, Region, CountryRegion
from tours.models import Tour, TourType


def set_slug():
    # for obj in City.objects.all():
    #     obj.slug = slugify(unidecode(obj.name))
    #     obj.save()
    for obj in Country.objects.all():
        obj.slug = slugify(unidecode(obj.name))
        obj.save()
    for obj in Region.objects.all():
        obj.slug = slugify(unidecode(obj.name))
        obj.save()
    for obj in CountryRegion.objects.all():
        obj.slug = slugify(unidecode(obj.name))
        obj.save()
    for obj in Tour.objects.all():
        if obj.name:
            obj.slug = slugify(unidecode(obj.name))
            obj.save()
    for obj in TourType.objects.all():
        obj.slug = slugify(unidecode(obj.name))
        obj.save()