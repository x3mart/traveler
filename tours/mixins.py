# from itertools import count
from datetime import timedelta, date
from django.forms import model_to_dict
from django.db import models
from django.shortcuts import get_object_or_404
from uritemplate import partial
from geoplaces.models import City
from django.utils.translation import gettext_lazy as _
from tours.models import TourAccomodation, TourPropertyType, TourType
from accounts.models import Expert, TeamMember
from languages.models import Language
from currencies.models import Currency
from tours.serializers import ImageSerializer, WallpaperSerializer, TOUR_REQUIRED_FIELDS


NOT_MODERATED_FIELDS = {'is_active', 'on_moderation', 'vacants_number', 'is_draft', 'discount_starts', 'discount_finish', 'discount_in_prc', 'discount', 'sold', 'watched'} 
CHECBOX_SET = {'is_guaranteed', 'is_active', 'postpay_on_start_day', 'scouting', 'animals_not_exploited', 'month_recurrent', 'flight_included', 'babies_alowed', 'on_moderation', 'week_recurrent', 'is_draft', 'instant_booking'}
EXCLUDED_FK_FIELDS = {'tour_basic', 'wallpaper', 'team_member', 'start_region', 'finish_region', 'start_country', 'finish_country', 'start_russian_region', 'finish_russian_region', 'start_city', 'finish_city'}


MTM_FIELDS = ['additional_types', 'tour_property_types', 'accomodation', 'tour_property_images', 'languages', 'tour_images',]


class TourMixin():
    def check_required_fieds(self, instance, current_section=None, errors={}):
        for section in TOUR_REQUIRED_FIELDS.keys():
            section_required_fields = TOUR_REQUIRED_FIELDS.get(section)
            empty_fields = [field for field in section_required_fields if not getattr(instance, field) or not hasattr(instance, field)]
            empty_mtm_fields = [field for field in set(section_required_fields).intersection(MTM_FIELDS) if not getattr(instance, field).exists()]
            empty_fields = empty_fields + empty_mtm_fields
            for field in empty_fields:
                if errors.get(field) and section == current_section:
                    errors[field].append(_("Обязательное поле"))
                elif not errors.get(field) and section == current_section:
                    errors[field] = [_("Обязательное поле")]
            if not instance.completed_sections and not empty_fields:
                instance.completed_sections = [section]
            elif section not in instance.completed_sections and not empty_fields:
                instance.completed_sections.append(section)
            elif section in instance.completed_sections and empty_fields:               
                instance.completed_sections.remove(section)
 
        
        if instance.prepay_amount and instance.prepay_in_prc and instance.prepay_amount < 15:
            errors['prepay_amount'] = [_("Предоплата не может быть меньше 15%")]
        elif instance.prepay_amount and instance.price and not instance.prepay_in_prc and instance.prepay_amount < instance.price*0.15:
            errors['prepay_amount'] = [_("Предоплата не может быть меньше") + f" {round(instance.price*0.15) + 1} {instance.currency.short_name if instance.currency else ''}"]
        return (instance, errors)

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
        additional_types = request.data.pop('additional_types')
        ids = map(lambda additional_type: additional_type.get('id'), additional_types)
        objects = self.get_mtm_objects(TourType, ids)
        instance.additional_types.set(objects)
    
    def set_property_types(self, request, instance):
        tour_property_types = request.data.pop('tour_property_types')
        ids = map(lambda tour_property_type: tour_property_type.get('id'), tour_property_types)
        objects = self.get_mtm_objects(TourPropertyType, ids)
        instance.tour_property_types.set(objects)
    
    def set_accomodation(self, request, instance):
        accomodations = request.data.pop('accomodation')
        ids = map(lambda accomodation: accomodation.get('id'), accomodations)
        objects = self.get_mtm_objects(TourAccomodation, ids)
        instance.accomodation.set(objects)
    
    def set_languages(self, request, instance=None):
        languages = request.data.pop('languages')
        ids = map(lambda language: language.get('id'), languages)
        objects = self.get_mtm_objects(Language, ids)
        instance.languages.set(objects)
    
    def set_mtm_from_str(self, request, field):
        field = request.data.get(field).rstrip(';')
        new_list = field.split(';')
        new_list = [x.strip() for x in new_list if x]
        return new_list 
    
    def get_expert(self, request):
        return get_object_or_404(Expert, pk=request.user.id)
    
    def set_fk_fields(self, request, instance):
        fk_fields = {field.name for field in instance._meta.get_fields() if isinstance(field, models.ForeignKey)} - EXCLUDED_FK_FIELDS
        for field in fk_fields:
            model = instance._meta.get_field(field).remote_field.model       
            if request.data.get(field) is not None:
                fk_id = request.data.get(field)['id']
                setattr(instance, field, model.objects.get(pk=fk_id))
        if request.data.get('team_member') is not None:
            fk_id = request.data.get('team_member')['id']
            setattr(instance, 'team_member', TeamMember.objects.get(pk=fk_id))
        start_city = request.data.get('start_city')
        finish_city = request.data.get('finish_city')
        if start_city and start_city.get('id'):
            city = City.objects.get(pk=start_city.get('id'))
            country = city.country
            country_region = city.country_region
            region = country.region if country else None
            setattr(instance, 'start_city', city)
            setattr(instance, 'start_region', region)
            setattr(instance, 'start_russian_region', country_region)
            setattr(instance, 'start_country', country)
        elif start_city and not start_city.get('id'):
            city = City.objects.create(name=start_city.get('full_name'))
            setattr(instance, 'start_city', city)
        if finish_city and finish_city.get('id'):
            city = City.objects.get(pk=finish_city.get('id'))
            country = city.country
            country_region = city.country_region
            region = country.region if country else None
            setattr(instance, 'finish_city', city)
            setattr(instance, 'finish_region', region)
            setattr(instance, 'finish_russian_region', country_region)
            setattr(instance, 'finish_country', country)
        elif finish_city and not finish_city.get('id') :
            city = City.objects.create(name=finish_city.get('full_name'))
            setattr(instance, 'finish_city', city)
        return instance
    
    def check_postpay_days_before_start(self, data):
        postpay_days_before_start = self.request.data.get('postpay_days_before_start')
        if postpay_days_before_start:
            postpay_days_before_start = int(postpay_days_before_start)
        if data.get('postpay_on_start_day'):
            data['postpay_days_before_start'] = timedelta(days=0)
        elif not data.get('postpay_on_start_day') and not postpay_days_before_start:
            data['postpay_on_start_day'] = True
            data['postpay_days_before_start'] = timedelta(days=0)
        else:
            postpay_days_before_start = postpay_days_before_start if postpay_days_before_start >= 5 else 5
            data['postpay_days_before_start'] = timedelta(days=postpay_days_before_start)
            data['postpay_on_start_day'] = False
        return data

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
        return instance

    def set_model_fields(self, data, instance):
        if self.request.META.get('CONTENT_TYPE') != 'application/json':
            not_sended_checbox = CHECBOX_SET - set(self.request.data.keys()).intersection(CHECBOX_SET)
            for item in not_sended_checbox:
                data.pop(item)
        data = self.check_postpay_days_before_start(data)
        if self.request.data.get('prepay_in_prc') is not None:
            data['prepay_in_prc'] = self.request.data.get('prepay_in_prc')
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


class TourSerializerMixin():
    def get_start_time(self, obj):
        if obj.start_time:
            return obj.start_time.strftime('%H:%M')
        else:
            return None

    def get_finish_time(self, obj):
        if obj.finish_time:
            return obj.finish_time.strftime('%H:%M')
        else:
            return None
    
    def get_discounted_price(self, obj):
        if obj.price and obj.discount and obj.discount_starts and  obj.discount_finish and obj.discount_starts < date.today() and  obj.discount_finish > date.today():
            return round(obj.price - obj.price*(obj.discount/100)) if obj.prepay_in_prc else obj.price - obj.discount
        else:
            return None

    def get_book_price(self, obj): 
        if obj.price:
            return round(obj.price*obj.prepay_amount/100) + 1 if obj.prepay_in_prc else obj.prepay_amount
        return None
    
    def get_daily_price(self, obj):
        discounted_price = self.get_discounted_price(obj)
        if discounted_price:
            return round(discounted_price/obj.duration)
        if obj.price and obj.duration: 
            return round(obj.price/obj.duration)
        return None

    def get_vacants_number(self, obj):
            return obj.vacants_number if obj.vacants_number < 5 else None
        
    def get_is_favourite(self, obj):
        return  None

    def get_is_new(self, obj):
        return  None

    def get_is_recomended(self, obj):
        return  None

    def get_discount(self, obj):
        if obj.price and obj.discount and obj.discount_starts and  obj.discount_finish and obj.discount_starts < date.today() and  obj.discount_finish > date.today():
            return round(obj.price - obj.price*(obj.discount/100)) if obj.prepay_in_prc else obj.price - obj.discount
        else:
            return None
    def get_main_impressions(self, obj):
        if obj.main_impressions:
            return '; '.join(obj.main_impressions)
        else:
            return ""
    def get_tour_included_services(self, obj): 
        if obj.tour_included_services:
            return '; '.join(obj.tour_included_services)
        else:
            return ""
    
    def get_tour_excluded_services(self, obj):
        if obj.tour_excluded_services is not None:
            return '; '.join(obj.tour_excluded_services)
        else:
            return "" 
    
    def get_required_fields(self, obj):
        required_fields = []
        for value in TOUR_REQUIRED_FIELDS:
            required_fields += TOUR_REQUIRED_FIELDS[value]
        return required_fields
    
    def get_postpay_days_before_start(self, obj):
        return obj.postpay_days_before_start.days