from django.contrib import admin

from tours.models import TourAddetionalService, TourExcludedService, TourIncludedService, TourPropertyImage, TourPropertyType, TourAdvanced, TourBasic, TourDay, TourDayImage, TourImage, TourType

# Register your models here.
admin.site.register(TourBasic)
admin.site.register(TourAdvanced)
admin.site.register(TourType)
admin.site.register(TourPropertyType)
admin.site.register(TourPropertyImage)
admin.site.register(TourImage)
admin.site.register(TourDay)
admin.site.register(TourDayImage)
admin.site.register(TourIncludedService)
admin.site.register(TourExcludedService)
admin.site.register(TourAddetionalService)
