from django.shortcuts import get_object_or_404
from tours.models import TourAccomodation, TourExcludedService, TourImpression, TourIncludedService, TourPropertyImage, TourPropertyType, TourType
from accounts.models import Expert
from languages.models import Language
from rest_framework.response import Response
from django.core.files.base import ContentFile

NOT_MODERATED_FIELDS = {'is_active', 'on_moderation', 'vacants_number', 'is_draft'}
CHECBOX_SET = {'is_guaranteed', 'is_active', 'postpay_on_start_day', 'scouting', 'animals_not_exploited', 'month_recurrent', 'flight_included', 'babies_alowed', 'on_moderation', 'week_recurrent', 'is_draft', 'instant_booking'}

class TourMixin():
    def get_mtm_objects(self, model, ids):
        objects = []
        for id in ids:
            objects.append(model.objects.get(pk=id))
        return objects

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
    
    def set_main_impressions(self, request, instance):
        main_impressions = request.data.get('main_impressions').split(',')
        main_impressions = map(lambda x: x.strip(), main_impressions)
        if instance.main_impressions.exists():
            instance.main_impressions.all().delete()
        impressions = []
        for impression in main_impressions:
            impressions.append(TourImpression(name=impression, tour=instance))
        TourImpression.objects.bulk_create(impressions)
    
    def set_tour_included_services(self, request, instance):
        tour_included_services = request.data.get('tour_included_services').split(',')
        tour_included_services = map(lambda x: x.strip(), tour_included_services)
        if instance.tour_included_services.exists():
            instance.tour_included_services.all().delete()
        services = []
        for service in tour_included_services:
            services.append(TourIncludedService(name=service, tour=instance))
        TourIncludedService.objects.bulk_create(services)
    
    def set_tour_excluded_services(self, request, instance):
        tour_excluded_services = request.data.get('tour_excluded_services').split(',')
        tour_excluded_services = map(lambda x: x.strip(), tour_excluded_services)
        if instance.tour_excluded_services.exists():
            instance.tour_excluded_services.all().delete()
        services = []
        for service in tour_excluded_services:
            services.append(TourExcludedService(name=service, tour=instance))
        TourExcludedService.objects.bulk_create(services)    
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_tour_direct_links(self, request, instance):
        tour_basic = instance.tour_basic
        tour_basic.direct_link = request.data.get('direct_link')
        tour_basic.save()
    
    def set_mtm_fields(self, request, instance):
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if request.data.get('tour_property_types'):
            self.set_property_types(request, instance)
        if request.data.get('languages'):
            self.set_languages(request, instance)
        if request.data.get('main_impressions'):
            self.set_main_impressions(request, instance)
        if request.data.get('tour_included_services'):
            self.set_tour_included_services(request, instance)
        if request.data.get('tour_excluded_services'):
            self.set_tour_excluded_services(request, instance)
        if request.data.get('direct_link'):
            self.set_tour_direct_links(request, instance)
        return (instance, list(request.data.keys()))

    def set_model_fields(self, data, instance):
        if self.request.META.get('CONTENT_TYPE') != 'application/json':
            not_sended_checbox = CHECBOX_SET - set(self.request.data.keys()).intersection(CHECBOX_SET)
            for item in not_sended_checbox:
                data.pop(item)
        for key, value in data.items():
            setattr(instance, key, value)
        return (instance, list(data.keys()))