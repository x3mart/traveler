from django.contrib import admin
from django.db.models.query import Prefetch
from tours.models import ImportantTitle, TourAccomodation, TourPropertyType, Tour, TourType, TourBasic

# Register your models here.
class TourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')
    list_display = ('name', 'expert', 'start_country', 'start_city', 'start_date', 'is_active', 'on_moderation', 'is_draft')
    list_editable =('is_active', 'on_moderation', 'is_draft')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = qs.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city')
        return qs
    
    @admin.display(description='Эксперт')
    def expert(self, obj):
        return obj.full_name


admin.site.register(Tour, TourAdmin)
admin.site.register(TourType)
admin.site.register(TourPropertyType)
admin.site.register(TourAccomodation)
admin.site.register(ImportantTitle)
