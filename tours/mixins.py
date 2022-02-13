from django.shortcuts import get_object_or_404
from tours.models import TourType
from accounts.models import Expert

class TourMixin():
    def set_additional_types(self, request, instance=None):
        if instance and instance.additional_types.exists():
            instance.additional_types.clear()
        additional_types = []
        additional_type_ids = request.data.get('additional_types').split(',')
        for additional_type_id in additional_type_ids:
            additional_types.append(TourType.objects.get(pk=additional_type_id))
        instance.additional_types.add(*tuple(additional_types))
        
    def get_basic_type(self, request):
        if request.data.get('basic_type'):
            return get_object_or_404(TourType, pk=request.data.get('basic_type'))
        return None
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_related_models(self, request, instance=None):
        if request.data.get('additional_types'):
            self.set_additional_types(request, instance)
        if self.get_basic_type(request):
            instance.basic_type = self.get_basic_type(request)
        if request.data.get('start_region'):
            instance.start_region_id = request.data.get('start_region')
        if request.data.get('finish_region'):
            instance.finish_region_id = request.data.get('finish_region')
        if request.data.get('start_country'):
            instance.start_country_id = request.data.get('start_country')
        if request.data.get('finish_country'):
            instance.finish_country_id = request.data.get('finish_country')
        if request.data.get('start_russian_region'):
            instance.start_russian_region_id = request.data.get('start_russian_region')
        if request.data.get('finish_russian_region'):
            instance.finish_russian_region_id = request.data.get('finish_russian_region')
        if request.data.get('start_city'):
            instance.start_city_id = request.data.get('start_city')
        if request.data.get('finish_city'):
            instance.finish_city_id = request.data.get('finish_city')
        if request.data.get('team_member'):
            instance.team_member_id = request.data.get('team_member')
        return instance