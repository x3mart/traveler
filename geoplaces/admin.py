from django.contrib import admin

from geoplaces.models import City, Country, Region, CountryRegion

# Register your models here.
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(CountryRegion)
admin.site.register(City)