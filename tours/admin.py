from django.contrib import admin

from tours.models import PropertyImage, PropertyType, TourAdvanced, TourBasic, TourDay, TourDayImage, TourImage, TourType

# Register your models here.
admin.site.register(TourBasic)
admin.site.register(TourAdvanced)
admin.site.register(TourType)
admin.site.register(PropertyType)
admin.site.register(PropertyImage)
admin.site.register(TourImage)
admin.site.register(TourDay)
admin.site.register(TourDayImage)
