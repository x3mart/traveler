from django.contrib import admin

from geoplaces.models import City, Country, Region, CountryRegion

# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_world_region', 'get_cities_count')
    list_filter = ('region',)
    ordering = ('name',)

    def get_queryset(self, request):
        return Country.objects.prefetch_related('region','cities')

    def get_world_region(self, obj):
        return obj.region.name if obj.region else ''
    
    def get_cities_count(self, obj):
        return obj.cities.count()



admin.site.register(Region)
admin.site.register(Country, CountryAdmin)
admin.site.register(CountryRegion)
admin.site.register(City)
# admin.site.register(VKCity)