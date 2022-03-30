from django.contrib import admin

from geoplaces.models import City, Country, Region, CountryRegion, VKCity

# Register your models here.
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(CountryRegion)
admin.site.register(City)
admin.site.register(VKCity)