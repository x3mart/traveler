from django.shortcuts import get_object_or_404
from tours.models import TourImpression, TourPropertyImage, TourPropertyType, TourType
from accounts.models import Expert
from languages.models import Language
from rest_framework.response import Response
from django.core.files.base import ContentFile

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
        if instance.additional_types.exists():
            instance.tour_property_types.clear()
        ids = request.data.get('tour_property_types')
        objects = self.get_mtm_objects(TourPropertyType, ids)
        instance.tour_property_types.add(*tuple(objects))
    
    def set_languages(self, request, instance=None):
        if instance.languages.exists():
            instance.languages.clear()
        ids = request.data.get('languages')
        objects = self.get_mtm_objects(Language, ids)
        instance.languages.add(*tuple(objects))
    
    def set_main_impressions(self, request, instance):
        main_impressions = request.data.get('main_impressions').split(',')
        map(lambda x: x.stripe(), main_impressions)
        if instance.main_impressions.exists():
            instance.main_impressions.all().delete()
        impressions = []
        for impression in main_impressions:
            impressions.append(TourImpression(name=impression, tour=instance))
        TourImpression.objects.bulk_create(impressions)
        
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_mtm_fields(self, request, instance):
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if request.data.get('tour_property_types'):
            self.set_property_types(request, instance)
        if request.data.get('languages'):
            self.set_languages(request, instance)
        if request.data.get('main_impressions'):
            self.set_main_impressions(request, instance)
        return instance

    def set_model_fields(self, data, instance):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance