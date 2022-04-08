from modeltranslation.translator import register, TranslationOptions
from .models import City, Region, Country, CountryRegion


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(CountryRegion)
class CountryRegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)