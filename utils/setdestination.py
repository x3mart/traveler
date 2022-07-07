
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







# def get_vk_countries():
#     url = 'https://api.vk.com/method/database.getCountries'
#     vk_data = {
#         'v':'5.131',
#         'count':1,
#         'need_all':1,
#         'access_token':VK_ACCESS_TOKEN,
#         'lang':'ru'
#     }
#     vk_response = requests.post(url, data=vk_data)
#     error = vk_response.json().get('error', None)
#     if error:
#         return Response(error, status=403)
#     vk_data['count'] = vk_response.json().get('response')['count']
#     vk_response = requests.post(url, data=vk_data)
#     for item in vk_response.json().get('response')['items']:
#         country = {}
#         country['name'] = item['title']
#         country['foreign_id'] = item['id']
#         Country.objects.get_or_create(**country)
#     return Country.objects.count()

# def get_vk_some(method, region_id=None, lang='en', country=1):
#     url = f'https://api.vk.com/method/database.{method}'
#     vk_data = {
#         'v':'5.131',
#         'count':10,
#         'need_all':1,
#         'access_token':VK_ACCESS_TOKEN,
#         'lang':lang,
#         'region_id':region_id,
#         'country_id':country
#     }
#     vk_response = requests.post(url, data=vk_data)
#     error = vk_response.json().get('error', None)
#     if error:
#         return print(error)
#     print(vk_response.json().get('response'))
#     return None

# def get_vk_country_regions():
#     url = 'https://api.vk.com/method/database.getRegions'
#     vk_data = {
#         'v':'5.131',
#         'count':1000,
#         'access_token':VK_ACCESS_TOKEN,
#         'lang':'ru'
#     }
#     country = Country.objects.get(foreign_id=1)
#     vk_data['country_id'] = 1
#     vk_response = requests.post(url, data=vk_data)
#     error = vk_response.json().get('error', None)
#     if error:
#         return Response(error, status=403)
#     for item in vk_response.json().get('response')['items']:
#         region = {}
#         region['name'] = item['title']
#         region['foreign_id'] = item['id']
#         region['country'] = country
#         CountryRegion.objects.get_or_create(**region)
#     return CountryRegion.objects.count()

# def get_vk_country_cities():
#     url = 'https://api.vk.com/method/database.getCities'
#     vk_data = {
#         'v':'5.131',
#         'count':1,
#         'need_all':1,
#         'access_token':VK_ACCESS_TOKEN,
#         'lang':'ru'
#     }
#     country = Country.objects.get(foreign_id=1)
#     for region in country.country_regions.all():
#         vk_data['country_id'] = 1
#         vk_data['region_id'] = region.foreign_id
#         vk_response = requests.post(url, data=vk_data)
#         error = vk_response.json().get('error', None)
#         if error:
#             return Response(error, status=403)
#         count = vk_response.json().get('response')['count']
#         print(count)
#         print(region.name)
#         x = 0
#         while x < count/500 + 1:
#             vk_data['count'] = 500
#             vk_data['offset'] = 500 * x
#             vk_response = requests.post(url, data=vk_data)
#             x += 1
#             cities = []
#             for item in vk_response.json().get('response')['items']:
#                 city = {}
#                 city['name'] = item['title']
#                 city['foreign_id'] = item['id']
#                 city['country'] = country
#                 city['country_region'] = region
#                 cities.append(VKCity(**city))
#             VKCity.objects.bulk_create(cities)
#             time.sleep(1)
#     return VKCity.objects.count()

# def set_russian_cities():
#     country = Country.objects.get(foreign_id=1)
#     for region in country.country_regions.all():
#         names = region.vkcities.values("name").distinct()
#         print(region.vkcities.count() - names.count())
#         print(region.name)
#         cities = []
#         for item in names:
#             city = {}
#             city['name'] = item['name']
#             city['country'] = country
#             city['country_region'] = region
#             cities.append(City(**city))
#         City.objects.bulk_create(cities)
#     return country.cities.count()


# def parse_country_json():
#     with open('pb_country.json', 'r') as data:
#         countries = json.load(data)['countries']
#         print(len(countries))
#         locations = {country["location"] for country in countries if country["location"] != ''}
#         regions = [Region(name=location) for location in locations]
#         Region.objects.bulk_create(regions)
#         countries_w_region = []
#         for region in Region.objects.all():
#             countries_w_region += [Country(name=country['name'], name_en=country['english'], counry_code=country['id'], region=region) for country in countries if country["location"] == region.name and country["id"] != 'RU' and country["id"] != 'UA']
#         countries_wo_region = [Country(name=country['name'], name_en=country['english'], counry_code=country['id']) for country in countries if country["location"] == '' and country["id"] != 'RU' and country["id"] != 'UA']
#         countries = countries_w_region + countries_wo_region
#         Country.objects.bulk_create(countries)

# def parse_city_json():
#     with open('pb_city.json', 'r') as data:
#         cities = json.load(data)['cities']
#         alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
#         cities = [city for city in cities if city["country"] != "RU" and city["country"] != "UA" and not alphabet.isdisjoint(city["name"].lower())]
#         for country in Country.objects.exclude(counry_code='RU').exclude(counry_code='UA'):
#             cities_w_country = list({city['name']:city for city in cities if city["country"] == country.counry_code}.values()) 
#             cities_w_country = [City(country=country, name=city['name'], name_en=city['english'], foreign_id=city['id']) for city in cities_w_country]
#             City.objects.bulk_create(cities_w_country)


# def set_distinct_city():
#     for city in City.objects.all():
#         cs = City.objects.filter(name=city.name).filter(country=city.country).filter(country_region=city.country_region)
#         if cs.count() > 1:
#             cs.exclude(pk=city.id).delete()




# class VKCity(models.Model):
#     name = models.CharField(_('Название'), max_length=255)
#     foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
#     country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='vkcities', verbose_name=_('Страна'), null=True, blank=True)
#     country_region = models.ForeignKey('CountryRegion', on_delete=models.CASCADE, related_name='vkcities', verbose_name=_('Регион Страны'), null=True, blank=True)

# class VKCityEn(models.Model):
#     name = models.CharField(_('Название'), max_length=255)
#     foreign_id = models.IntegerField(_('Сторонний ключ'), null=True, blank=True)
#     country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='vkcities_en', verbose_name=_('Страна'), null=True, blank=True)
#     country_region = models.ForeignKey('CountryRegion', on_delete=models.CASCADE, related_name='vkcities_en', verbose_name=_('Регион Страны'), null=True, blank=True)