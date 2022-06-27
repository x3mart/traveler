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
        self.filter_data = self.get_filter_data(queryset, request)
        return super().paginate_queryset(queryset, request, view)
    
    def get_field_filter(self, filters, field):
        filter_set = {}
        for filter in filters:
            if filter != field:
                filter_set.upgrade(filters[filter])
        return filter_set
    
    def get_filter_data(self, queryset, request):
        tour_basic = TourBasic.objects.prefetch_related('expert')
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        active_tours = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).annotate(
                discounted_price = Case(
                    When(Q(discount__isnull=True) or Q(discount=0), then=F('price')),
                    When(~Q(discount__isnull=True) and ~Q(discount_starts__isnull=True) and Q(discount__gt=0) and Q(discount_starts__gte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=True), then=F('price') - F('price')*F('discount')/100),
                    When(~Q(discount__isnull=True) and Q(discount__gt=0) and Q(discount_starts__lte=datetime.today()) and Q(discount_finish__gte=datetime.today()) and Q(discount_in_prc=False), then=F('price') - F('discount')),
                )
            )
        filters={}
        params = dict(request.query_params)
        for type in params:
            if params['type'][0] and type == 'price':
                value = params[type][0].split(',')
                filters.append({'price':{'discounted_price__gte':value[0], 'discounted_price__lte':value[1]}})
            elif type == 'price':
                value = params[type][0].split(',')
                filters.append({'languages':{'languages_in':value}})
            elif type == 'age':
                value = params[type][0].split(',')
                filters.append({'age':{'age_starts__lte':value[0], 'age_ends__gte':value[1]}})
            elif type == 'duration':
                value = params[type][0].split(',')
                filters.append({'duration':{'duration__gte':value[0], 'duration__lte':value[1]}})
                
        qs_tour_types = active_tours.filter(**self.get_field_filter(filters, 'tour_types'))
        tour_types = TourType.objects.filter(Q(tours_by_basic_type__in=qs_tour_types) | Q(tours_by_additional_types__in=qs_tour_types)).order_by('name').values('name', 'id').distinct()
        qs = active_tours.filter(**self.get_field_filter(filters, 'languages'))
        languages = Language.objects.filter(tours__in=qs).order_by('name').values('name', 'id').distinct()
        property_type = TourPropertyType.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        accomodation = TourAccomodation.objects.filter(tours__in=queryset).order_by('name').values('name', 'id').distinct()
        qs = active_tours.filter(**self.get_field_filter(filters, 'price'))
        price = qs.aggregate(Min('discounted_price'), Max('discounted_price'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'age'))
        age = qs.aggregate(Min('age_starts'), Max('age_ends'))
        qs = active_tours.filter(**self.get_field_filter(filters, 'duration'))
        duration = qs.aggregate(Min('duration'), Max('duration'))
        aggregations = queryset.aggregate( Max('vacants_number'), Max('tour_basic__rating'), Max('difficulty_level'), Max('comfort_level'))
        TourBasic.objects.filter(tours__in=queryset).aggregate(Max('rating'))
        
        filter_data = [
            {'title': 'Тип тура', 'type':'tour_types', 'data': tour_types},
            {'title': 'Языки группы', 'type':'languages', 'data': languages},
            {'title': 'Проживание', 'type':'property_type', 'data': property_type},
            {'title': 'Размещение', 'type':'accomodation', 'data': accomodation},
            {'title': 'Цена', 'type':'price', 'filter_type': 'range', 'data': [price['discounted_price__min'], price['discounted_price__max']]},
            {'title': 'Допустимый возраст', 'type':'age', 'filter_type': 'range', 'data': [age['age_starts__min'], age['age_ends__max']]},
            {'title': 'Продолжительность тура', 'type':'duration_min', 'filter_type': 'range', 'data': [duration['duration__min'],duration['duration__max']]},

            {'title': 'Свободные места', 'type':'vacants_number', 'data': aggregations['vacants_number__max']},
            {'title': 'Рейтинг', 'type':'rating', 'data': aggregations['tour_basic__rating__max']},
            {'title': 'Сложность', 'type':'difficulty_level', 'data': aggregations['difficulty_level__max']},
            {'title': 'Комфорт', 'type':'comfort_level', 'data': aggregations['comfort_level__max']}
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