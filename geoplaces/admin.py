from django.contrib import admin

from geoplaces.models import City, Country, Destination, Region

# Register your models here.
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_world_region')
    list_filter = ('region',)
    ordering = ('name',)

    def get_queryset(self, request):
        return Destination.objects.prefetch_related('region','cities')

    def get_world_region(self, obj):
        return obj.region.name if obj.region else ''
    
    # def get_cities_count(self, obj):
    #     return obj.cities.count()



admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Destination)
admin.site.register(City)
# admin.site.register(VKCity)