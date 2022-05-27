from django.contrib import admin
from django.db.models.query import Prefetch
from tours.models import ImportantTitle, ModeratedTour, TourAccomodation, TourPropertyType, Tour, TourType, TourBasic

# Register your models here.
class TourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')
    list_display = ('name', 'expert', 'start_country', 'start_city', 'start_date', 'is_active', 'on_moderation', 'is_draft', 'direct_link')
    # list_editable =('is_active', 'on_moderation', 'is_draft')
    list_filter = ('is_active', 'on_moderation', 'is_draft', 'tour_basic__expert')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = qs.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city')
        return qs
    
    @admin.display(description='Эксперт')
    def expert(self, obj):
        return obj.tour_basic.expert.full_name

class ModeratedTourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')
    list_display = ('name', 'expert', 'start_country', 'start_city', 'start_date', 'is_active', 'on_moderation', 'is_draft', 'direct_link')
    # list_editable =('is_active', 'on_moderation', 'is_draft')
    list_filter = ('tour_basic__expert',)
    list_display_links = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = qs.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city').filter(on_moderation=True)
        return qs
    
    @admin.display(description='Эксперт')
    def expert(self, obj):
        return obj.tour_basic.expert.full_name


admin.site.register(Tour, TourAdmin)
admin.site.register(ModeratedTour, ModeratedTourAdmin)
admin.site.register(TourType)
admin.site.register(TourPropertyType)
admin.site.register(TourAccomodation)
admin.site.register(ImportantTitle)
admin.site.register(TourBasic)
