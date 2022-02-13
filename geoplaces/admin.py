from django.contrib import admin

from geoplaces.models import City, Country, Region, RussianRegion

# Register your models here.
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(RussianRegion)
admin.site.register(City)