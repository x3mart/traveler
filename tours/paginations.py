from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Q, Max, Min, When, Case
from datetime import timedelta, datetime
from django.db.models.query import Prefetch

from languages.models import Language
from orders.models import Order
from tours.models import Tour, TourAccomodation, TourBasic, TourPropertyType, TourType

class TourResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data,
            'filter_set': self.filter_data
        })
    
    def paginate_queryset(self, queryset, request, view=None):
        self.filter_data = []
        if view.action == 'list':
            self.filter_data = self.get_filter_data(queryset, request)
        return super().paginate_queryset(queryset, request, view)
    
    def get_q_filters(self, filters, field, type=None):
        q_filter = Q()
        for filter in filters:
            if filter != field and filter == 'tour_types':
                q_filter = filters[filter]
        return q_filter
    
    def get_field_filter(self, filters, field, type=None):
        filter_set = {}
        for filter in filters:
            if filter != field and filter != 'tour_types':
                filter_set.update(filters[filter])
            
        return filter_set
    
    def get_filter_data(self, queryset, request):
        active_tours = Tour.objects.prefetched().in_sale().with_discounted_price()
        filters={}
        params = dict(request.query_params)
        for type in params:
            if type == 'price':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'price':{'discounted_price__gte':value[0], 'discounted_price__lte':value[1]}})
            elif type == 'languages':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'languages':{'languages__in':value}})
            elif type == 'age':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'age':{'age_starts__lte':value[0], 'age_ends__gte':value[1]}})
            elif type == 'duration':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'duration':{'duration__gte':value[0], 'duration__lte':value[1]}})
            elif type == 'vacants_number':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'vacants_number':{'vacants_number__gte':value[0], 'vacants_number__lte':value[1]}})
            elif type == 'rating':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'rating':{'tour_basic__rating__gte':value[0]}})
            elif type == 'tour_types':
                value = params[type][0].split(',')
                if value[0]:
                    filters.update({'tour_types': Q(basic_type__in=value) | Q(additional_types__in=value)})
                
        qs_tour_types = active_tours.filter(**self.get_field_filter(filters, 'tour_types')).filter(self.get_q_filters(filters, 'tour_types'))
        tour_types = TourType.objects.filter(Q(tours_by_basic_type__in=qs_tour_types) | Q(tours_by_additional_types__in=qs_tour_types)).order_by('name').values('name', 'id').distinct()
        qs = active_tours.filter(**self.get_field_filter(filters, 'languages')).filter(self.get_q_filters(filters, 'languages'))
        languages = Language.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        property_type = TourPropertyType.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        accomodation = TourAccomodation.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        qs = active_tours.filter(**self.get_field_filter(filters, 'price')).filter(self.get_q_filters(filters, 'price'))
        price = qs.aggregate(Min('discounted_price'), Max('discounted_price'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'age')).filter(self.get_q_filters(filters, 'age'))
        age = qs.aggregate(Min('age_starts'), Max('age_ends'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'duration')).filter(self.get_q_filters(filters, 'duration'))
        duration = qs.aggregate(Min('duration'), Max('duration'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'vacants_number')).filter(self.get_q_filters(filters, 'vacants_number'))
        vacants_number = qs.aggregate(Min('vacants_number'), Max('vacants_number'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'difficulty_level')).filter(self.get_q_filters(filters, 'difficulty_level'))
        difficulty_level = qs.aggregate(Max('difficulty_level'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'comfort_level')).filter(self.get_q_filters(filters, 'comfort_level'))
        comfort_level = qs.aggregate(Max('comfort_level'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'rating')).filter(self.get_q_filters(filters, 'rating'))
        rating = qs.aggregate(Max('tour_basic__rating'))
        
        filter_data = [
            {'title': '?????? ????????', 'type':'tour_types', 'data': tour_types},
            {'title': '?????????? ????????????', 'type':'languages', 'data': languages},
            {'title': '????????????????????', 'type':'property_type', 'data': property_type},
            {'title': '????????????????????', 'type':'accomodation', 'data': accomodation},
            {'title': '????????', 'type':'price', 'filter_type': 'range', 'data': [price['discounted_price__min'], price['discounted_price__max']]},
            {'title': '???????????????????? ??????????????', 'type':'age', 'filter_type': 'range', 'data': [age['age_starts__min'], age['age_ends__max']]},
            {'title': '?????????????????????????????????? ????????', 'type':'duration', 'filter_type': 'range', 'data': [duration['duration__min'],duration['duration__max']]},

            {'title': '?????????????????? ??????????', 'type':'vacants_number', 'filter_type': 'range', 'data': [vacants_number['vacants_number__min'],vacants_number['vacants_number__max']]},
            {'title': '??????????????', 'type':'rating', 'filter_type': 'rating', 'data': rating['tour_basic__rating__max']},
            {'title': '??????????????????', 'type':'difficulty_level', 'filter_type': 'radio', 'data': difficulty_level['difficulty_level__max']},
            {'title': '??????????????', 'type':'comfort_level', 'filter_type': 'radio', 'data': comfort_level['comfort_level__max']}
        ]
        # if len(request.query_params):
        #     params = dict(request.query_params)
        #     params = {key:params[key] for key in params if key != list(request.query_params)[-1] and params[key]} 
        #     # params.pop(list(request.query_params)[-1])
        #     filters = {}
        #     for key in params:
        #         if params[key][0]:
        #             print(key, params[key][0].split(','))
        #             if key == 'tour_types':
        #                 pass
        #             else:
        #                 filters.update({f"{key}__in":params[key][0].split(',')})
        #     print(filters)
        #     tours = Tour.objects.filter(**filters)
        #     print(tours)
        return filter_data