from django.shortcuts import get_object_or_404
from tours.models import TourPropertyImage, TourPropertyType, TourType
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
    
    def set_tour_property_images(self, request, instance):
        images = request.FILES.getlist('tour_property_images')
        print(images)
        objects = []
        for image in images:
            data = {'image':ContentFile(image), 'tour_id':instance.id}

            print(data)
            TourPropertyImage.objects.create(**data)

    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_mtm_fields(self, request, instance):
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if request.data.get('tour_property_types'):
            self.set_property_types(request, instance)
        if request.data.get('languages'):
            self.set_languages(request, instance)
        # if request.data.get('tour_property_images'):
        #     self.set_tour_property_images(request, instance)
        return instance

    def set_model_fields(self, data, instance):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance