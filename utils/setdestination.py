
from unicodedata import name
from geoplaces.models import City, Country, CountryRegion, Destination, Region
from tours.models import Tour

def set_destinations():
    for country_region_id in CountryRegion.objects.filter(country__name__in=['Россия']).values_list('id', flat=True):
        Destination.objects.create(country_region_id=country_region_id)
    for country_id in Country.objects.exclude(name__in=['Россия', 'Россия2']).values_list('id', flat=True):
        Destination.objects.create(country_id=country_id)

def set_tour_destinations():
    for tour in Tour.objects.exclude(start_city__isnull=True):
        tour.save()

def russin_regions_to_country():
    russia = Region.objects.get(name='Россия')
    for country_region in CountryRegion.objects.filter(country__name__in=['Россия']):
        country = Country.objects.create(name=country_region.name, slug=country_region.slug, region=russia)
        City.objects.filter(country_region_id=country_region.id).update(country_id=country.id)