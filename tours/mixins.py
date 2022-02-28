from django.shortcuts import get_object_or_404
from tours.models import TourAccomodation, TourExcludedService, TourImpression, TourIncludedService, TourPropertyImage, TourPropertyType, TourType
from accounts.models import Expert
from languages.models import Language
from rest_framework.response import Response
from django.core.files.base import ContentFile

NOT_MODERATED_FIELDS = {'is_active', 'on_moderation', 'vacants_number', 'is_draft', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'sold', 'watched'} 
CHECBOX_SET = {'is_guaranteed', 'is_active', 'postpay_on_start_day', 'scouting', 'animals_not_exploited', 'month_recurrent', 'flight_included', 'babies_alowed', 'on_moderation', 'week_recurrent', 'is_draft', 'instant_booking'}

class TourMixin():
    def get_mtm_objects(self, model, ids):
        objects = []
        for id in ids:
            objects.append(model.objects.get(pk=id))
        return objects
    
    def get_mtm_set(self, obj_set): 
        return set(obj_set.all().values_list('name', flat=True))

    def set_additional_types(self, request, instance):
        if instance.additional_types.exists():
            instance.additional_types.clear()
        ids = request.data.get('additional_types')
        objects = self.get_mtm_objects(TourType, ids)
        instance.additional_types.add(*tuple(objects))
    
    def set_property_types(self, request, instance):
        if instance.tour_property_types.exists():
            instance.tour_property_types.clear()
        ids = request.data.get('tour_property_types')
        objects = self.get_mtm_objects(TourPropertyType, ids)
        instance.tour_property_types.add(*tuple(objects))
    
    def set_accomodation(self, request, instance):
        if instance.accomodation.exists():
            instance.accomodation.clear()
        ids = request.data.get('accomodation')
        objects = self.get_mtm_objects(TourAccomodation, ids)
        instance.accomodation.add(*tuple(objects))
    
    def set_languages(self, request, instance=None):
        if instance.languages.exists():
            instance.languages.clear()
        ids = request.data.get('languages')
        objects = self.get_mtm_objects(Language, ids)
        instance.languages.add(*tuple(objects))
    
    def set_mtm_from_str(self, request, instance, field, model, updated_fields):
        new_set = request.data.get(field).split(',')
        new_set = set(map(lambda x: x.strip(), new_set))
        if getattr(instance, field).exists():
            old_set = self.get_mtm_set(getattr(instance, field))
            to_delete = old_set - new_set
            to_add = new_set - old_set
            getattr(instance, field).filter(name__in=to_delete).delete()
        else:
            to_add = new_set
            to_delete = None
        objs = []
        for name in to_add:
            objs.append(model(name=name, tour=instance))
        model.objects.bulk_create(objs)
        if to_delete or to_add:
            updated_fields.add(field) 
        return updated_fields 
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_tour_direct_links(self, request, instance):
        tour_basic = instance.tour_basic
        tour_basic.direct_link = request.data.get('direct_link')
        tour_basic.save()
    
    def set_mtm_fields(self, request, instance):
        updated_fields = set()
        if request.data.get('additional_types') is not None:
            self.set_additional_types(request, instance)
        if request.data.get('tour_property_types') is not None:
            self.set_property_types(request, instance)
        if request.data.get('accomodation') is not None:
            self.set_accomodation(request, instance)
        if request.data.get('languages') is not None:
            self.set_languages(request, instance)
        if request.data.get('main_impressions') is not None:
            updated_fields = self.set_mtm_from_str(request, instance, 'main_impressions', TourImpression, updated_fields)
        if request.data.get('tour_included_services') is not None:
            updated_fields = self.set_mtm_from_str(request, instance, 'tour_included_services', TourIncludedService, updated_fields)
        if request.data.get('tour_excluded_services') is not None:
            updated_fields = self.set_mtm_from_str(request, instance, 'tour_excluded_services', TourExcludedService, updated_fields)
        if request.data.get('direct_link') is not None:
            self.set_tour_direct_links(request, instance)
        return (instance, updated_fields)

    def set_model_fields(self, data, instance):
        if self.request.META.get('CONTENT_TYPE') != 'application/json':
            not_sended_checbox = CHECBOX_SET - set(self.request.data.keys()).intersection(CHECBOX_SET)
            for item in not_sended_checbox:
                data.pop(item)
        for key, value in data.items():
            setattr(instance, key, value)
        return instance