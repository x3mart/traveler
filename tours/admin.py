from django.contrib import admin

from tours.models import TourAccomodation, TourPropertyType, Tour, TourType

# Register your models here.
admin.site.register(Tour)
admin.site.register(TourType)
admin.site.register(TourPropertyType)
admin.site.register(TourAccomodation)
