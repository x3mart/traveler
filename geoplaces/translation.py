from modeltranslation.translator import register, TranslationOptions
from .models import City, Region, Destination


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Destination)
class DestinationTranslationOptions(TranslationOptions):
    fields = ('name',)

# @register(Country)
# class DestinationTranslationOptions(TranslationOptions):
#     fields = ('name',)

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)