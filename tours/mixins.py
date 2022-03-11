from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from uritemplate import partial
from tours.models import TourAccomodation, TourPropertyType, TourType
from accounts.models import Expert
from languages.models import Language
from tours.serializers import ImageSerializer, WallpaperSerializer


NOT_MODERATED_FIELDS = {'is_active', 'on_moderation', 'vacants_number', 'is_draft', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'sold', 'watched'} 
CHECBOX_SET = {'is_guaranteed', 'is_active', 'postpay_on_start_day', 'scouting', 'animals_not_exploited', 'month_recurrent', 'flight_included', 'babies_alowed', 'on_moderation', 'week_recurrent', 'is_draft', 'instant_booking'}

class TourMixin():
    def check_set_tour_field_for_moderation(self, instance, field):
        if field not in NOT_MODERATED_FIELDS and instance.is_active:
            instance.is_active = False
            instance.on_moderation = True

    def get_instance_image_data(self, request):
        instance = self.get_object()
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        return (instance, data)
    
    def get_instance_wallpaper_data(self, request):
        instance = self.get_object()
        serializer = WallpaperSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        return (instance, data)

    def get_mtm_objects(self, model, ids):
        return model.objects.filter(pk__in=ids)
    
    def get_mtm_set(self, obj_set): 
        return set(obj_set.all().values_list('name', flat=True))

    def set_additional_types(self, request, instance):
        ids = request.data.get('additional_types')
        objects = self.get_mtm_objects(TourType, ids)
        instance.additional_types.set(objects)
    
    def set_property_types(self, request, instance):
        ids = request.data.get('tour_property_types')
        objects = self.get_mtm_objects(TourPropertyType, ids)
        instance.tour_property_types.set(objects)
    
    def set_accomodation(self, request, instance):
        ids = request.data.get('accomodation')
        objects = self.get_mtm_objects(TourAccomodation, ids)
        instance.accomodation.set(objects)
    
    def set_languages(self, request, instance=None):
        ids = request.data.get('languages')
        objects = self.get_mtm_objects(Language, ids)
        instance.languages.set(objects)
    
    def set_mtm_from_str(self, request, field):
        new_list = request.data.get(field.rstrip(';')).split(';')
        new_list = list(map(lambda x: x.strip(), new_list))
        return new_list 
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_tour_direct_links(self, request, instance):
        tour_basic = instance.tour_basic
        tour_basic.direct_link = request.data.get('direct_link')
        tour_basic.save()

    def set_mtm_fields(self, request, instance):       
        if request.data.get('additional_types') is not None:
            self.set_additional_types(request, instance)
        if request.data.get('tour_property_types') is not None:
            self.set_property_types(request, instance)
        if request.data.get('accomodation') is not None:
            self.set_accomodation(request, instance)
        if request.data.get('languages') is not None:
            self.set_languages(request, instance)
        if request.data.get('main_impressions') is not None:
            instance.main_impressions = self.set_mtm_from_str(request, 'main_impressions')
        if request.data.get('tour_included_services') is not None:
            instance.tour_included_services = self.set_mtm_from_str(request, 'tour_included_services')
        if request.data.get('tour_excluded_services') is not None:
            instance.tour_excluded_services = self.set_mtm_from_str(request, 'tour_excluded_services')
        if request.data.get('direct_link') is not None:
            self.set_tour_direct_links(request, instance)
        return instance

    def set_model_fields(self, data, instance):
        if self.request.META.get('CONTENT_TYPE') != 'application/json':
            not_sended_checbox = CHECBOX_SET - set(self.request.data.keys()).intersection(CHECBOX_SET)
            for item in not_sended_checbox:
                data.pop(item)
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
    
    def copy_tour_mtm(self, old_instance, instance):
        additional_types = old_instance.additional_types.all()
        tour_property_types = old_instance.tour_property_types.all()
        accomodation = old_instance.accomodation.all()
        tour_property_images = old_instance.tour_property_images.all()
        languages = old_instance.languages.all()
        tour_images = old_instance.tour_images.all()
        instance.additional_types.add(*additional_types)
        instance.tour_property_types.add(*tour_property_types)
        instance.accomodation.add(*accomodation)
        instance.tour_property_images.add(*tour_property_images)
        instance.languages.add(*languages)
        instance.tour_images.add(*tour_images)