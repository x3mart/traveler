from django.contrib import admin
from utils import tokenizator
from django.utils.safestring import mark_safe
from django.db.models.query import Prefetch
from tours.models import ImportantTitle, ModeratedTour, TourAccomodation, TourPropertyType, Tour, TourType, TourBasic

# Register your models here.
class TourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')
    list_display = ('name', 'expert', 'start_destination', 'start_city', 'start_date', 'is_active', 'on_moderation', 'is_draft', 'direct_link')
    # list_editable =('is_active', 'on_moderation', 'is_draft')
    list_filter = ('is_active', 'on_moderation', 'is_draft', 'tour_basic__expert')
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = qs.prefetch_related(prefetch_tour_basic, 'start_destination', 'start_city')
        return qs
    
    @admin.display(description='Эксперт')
    def expert(self, obj):
        return obj.tour_basic.expert.full_name

class ModeratedTourAdmin(admin.ModelAdmin):
    readonly_fields=('start_city', 'finish_city')
    list_display = ('linked_name', 'expert', 'start_destination', 'start_city', 'start_date',)
    # list_editable =('is_active', 'on_moderation', 'is_draft')
    list_filter = ('tour_basic__expert',)
    list_display_links = None

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        qs = qs.prefetch_related(prefetch_tour_basic, 'start_destination', 'start_city').filter(on_moderation=True)
        return qs
    
    @admin.display(description='Название')
    def linked_name(self, obj):
        return mark_safe(f'<a href="https://traveler.market/moderation/{obj.id}/?token={tokenizator.create_token(self.request.user.id)}">{obj.name}</a>')
    
    @admin.display(description='Эксперт')
    def expert(self, obj):
        return obj.tour_basic.expert.full_name

class TourTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tour, TourAdmin)
admin.site.register(ModeratedTour, ModeratedTourAdmin)
admin.site.register(TourType, TourTypeAdmin)
admin.site.register(TourPropertyType)
admin.site.register(TourAccomodation)
admin.site.register(ImportantTitle)
admin.site.register(TourBasic)
