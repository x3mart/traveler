from django.contrib import admin

from tours.models import ImportantTitle, TourAccomodation, TourPropertyType, Tour, TourType

# Register your models here.
class TourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')



admin.site.register(Tour, TourAdmin)
admin.site.register(TourType)
admin.site.register(TourPropertyType)
admin.site.register(TourAccomodation)
admin.site.register(ImportantTitle)
