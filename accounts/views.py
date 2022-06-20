from django.db.models import F, Q
from datetime import timedelta, datetime
from rest_framework.serializers import ValidationError
from django.shortcuts import redirect
from rest_framework.decorators import action
from accounts.permissions import TeamMemberPermission, UserPermission, CustomerPermission, ExpertPermission
from accounts.serializers import AvatarSerializer, CustomerMeSerializer, EmailActivationSerializer, ExpertListSerializer, ExpertMeSerializer, ExpertSerializer, TeamMemberSerializer, UserSerializer, CustomerSerializer
from rest_framework import viewsets, status
from accounts.models import Expert, PhoneConfirm, TeamMember, User, Customer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views import View
from django.http import JsonResponse
from django.template.response import TemplateResponse
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.db.models.query import Prefetch
from djoser import utils
from djoser.conf import settings
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string
from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from bankdetails.models import BankTransaction, DebetCard, Scan
from bankdetails.serializers import BankTransactionSerializer, DebetCardSerializer, ScanSerializer
from django.utils.translation import gettext_lazy as _
from geoplaces.models import Country
from tours.models import Tour, TourBasic
from tours.mixins import TourMixin
import random
import json
from traveler.settings import FLASH_CALL
from utils.times import get_timestamp_str
from rest_framework import serializers

from verificationrequests.models import VerificationRequest
from verificationrequests.serializers import VerificationRequestlSerializer


class ConfirmEmailThread(threading.Thread, BaseEmailMessage):
    def __init__(self, user, request):
        self.user = user
        self.request = request
        threading.Thread.__init__(self)
        BaseEmailMessage.__init__(self, request, template_name='email_confirm.html')
    
    def run(self):
        subject = 'Подтверждение почты'
        context = self.get_context_data()
        context["uid"] = utils.encode_uid(self.user.pk)
        context["token"] = default_token_generator.make_token(self.user)
        # context["domain"] = self.request.META.get('REMOTE_HOST')
        context["site_name"] = 'https://traveler.market/'
        context["url"] = settings.ACTIVATION_URL.format(**context)
        message_html = render_to_string("email_confirm.html", context)
        send_mail(subject, "message", 'info@traveler.market', [self.user.email,], html_message=message_html,)
        # print(self.request.META.get('HTTP_REFERER'))


class RedirectSocial(View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        return JsonResponse(json_obj)

class PasswordRecovery(View):
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'resetpassword.html')
    
    def post(self, request, *args, **kwargs):
        data = {'email': request.POST.get('email')}
        response = requests.post('http://x3mart.ru/auth/users/reset_password/', json=data)
        if response.status_code == 204:
            return TemplateResponse(request, 'resetpassword_success.html', {'email':request.POST.get('email')})
        return TemplateResponse(request, 'resetpassword _error.html')


class PasswordRecoveryConfirm(View):
    def get(self, request, uid, token, *args, **kwargs):
        return TemplateResponse(request, 'enter_new_ password.html')
    
    def post(self, request, uid, token, *args, **kwargs):
        data = request.POST
        data = {'uid': uid, 'token':token, 'new_password':data.get('password'), 're_new_password':data.get('re_password')}
        response = requests.post('http://x3mart.ru/auth/users/reset_password_confirm/', json=data)
        if response.status_code == 204:
            return redirect('http://x3mart.ru/admin/')
        return TemplateResponse(request, 'enter_new_ password.html', {'uid':response.json().get('uid'), 'token':response.json().get('token'), 'new_password':response.json().get('new_password')})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'expert'):
            token['user_status'] = 'experts'
        elif hasattr(user, 'customer'):
            token['user_status'] = 'customers'
        else:
            token['user_status'] = 'staff'
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if hasattr(self.user, 'expert'):
            data['user_status'] = 'experts'
        elif hasattr(self.user, 'customer'):
            data['user_status'] = 'customers'
        elif self.user.is_staff:
            data['user_status'] = 'staff'
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_me(self, request,  *args, **kwargs):
    self.get_object = self.get_instance
    if request.method == 'GET':
        return self.retrieve(request, *args, **kwargs)
    elif request.method == 'PUT':
        return self.update(request, *args, **kwargs)
    elif request.method == 'PATCH':
        return self.partial_update(request, *args, **kwargs)
    elif request.method == 'DELETE':
        return self.destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]


    def get_queryset(self):
        return super().get_queryset()
    
class ExpertViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [ExpertPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['tours_count', 'tours_avg_rating']
    filterset_fields = ['first_name', 'last_name']
    token_generator = default_token_generator

    def get_instance(self):
        return self.queryset.get(pk=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExpertListSerializer
        if self.action == 'me':
            return ExpertMeSerializer
        if self.action == 'confirm_email':
            return EmailActivationSerializer
        if self.action == 'debet_card':
            return DebetCardSerializer
        if self.action == 'bank_transaction':
            return BankTransactionSerializer
        if self.action == 'scans':
            return ScanSerializer
        if self.action == 'verification':
            return VerificationRequestlSerializer
        if self.action == 'send_confirmation_call':
            return UserSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        if self.request.data.get('referral'):
            pass
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if self.request.data.get('languages'):
            expert = self.get_object()
            self.set_languages(self.request, expert) 
        return super().perform_update(serializer)
    
    @action(["get"], detail=True)
    def details(self, request, *args, **kwargs):
        expert = self.get_object()
        tour_basic = TourBasic.objects.all()
        prefetch_tour_basic = Prefetch('tour_basic', tour_basic)
        expert_tours = Tour.objects.prefetch_related(prefetch_tour_basic, 'start_country', 'start_city', 'wallpaper', 'currency').only('id', 'name', 'start_date', 'start_country', 'start_city', 'price', 'discount', 'duration', 'tour_basic', 'wallpaper', 'vacants_number', 'currency').filter(is_active=True).filter(direct_link=False).filter(Q(booking_delay__lte=F('start_date') - datetime.today().date() - F('postpay_days_before_start'))).filter(tour_basic__expert=expert)[:3]
        expert.expert_tours = expert_tours
        return Response(ExpertSerializer(expert, many=False, context={'request':request}).data, status=200)

    @action(['get', 'put', 'patch', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):
        return get_me(self, request, *args, **kwargs)
    
    @action(['patch', 'delete'], detail=False)
    def avatar(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = AvatarSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
            expert = Expert.objects.get(pk=request.user.id)
            expert.avatar = data['avatar']
            expert.save()
        elif request.method == 'DELETE':
            expert = Expert.objects.get(pk=request.user.id)
            expert.avatar = None
            expert.save()
        return Response(ExpertMeSerializer(expert, context={'request':request}).data, status=status.HTTP_200_OK)
    
    @action(["post"], detail=False)
    def send_confirmation_email(self, request, *args, **kwargs):
        user = request.user
        ConfirmEmailThread(user, request).start()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(["post"], detail=False)
    def confirm_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expert = Expert.objects.get(pk=serializer.user.id)
        expert.email_confirmed = True
        expert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(["patch"], detail=True)
    def send_confirmation_call(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user.phone = data['phone']
        user.save()
        code =  str(random.randint(1000,9999))
        data = json.dumps([{
                        "channelType": "FLASHCALL",
                        "senderName": "Santa",
                        "destination": str(user.phone).lstrip('+'),
                        "content": code
                        }])
        # time = get_timestamp_str()
        # token_str = f"call-password/start-password-call\n{time}\n{KEY_NEWTEL}\n{data}\n{WRITE_KEY}".encode('utf-8')
        # token = KEY_NEWTEL + time + hashlib.sha256(token_str).hexdigest()
        headers = {"Authorization": FLASH_CALL, "Content-Type": "application/json"}
        response = requests.post('https://direct.i-dgtl.ru/api/v1/message', data=data, headers=headers)
        if not response.json().get('error'):
            PhoneConfirm.objects.create(user_id=user.id, code=code)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors':response.json().get('error')}, status=403)
    
    @action(["post"], detail=True)
    def check_confirmation_code(self, request, *args, **kwargs):
        user = self.get_object()
        confirme = user.phone_confirms.filter(code=request.data.get('code'))
        if confirme.exists():
            user.phone_confirmed = True
            user.save()
            user.phone_confirms.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'code':['Неверный код'],}, status=403)
        

    @action(["patch"], detail=True)
    def debet_card(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if hasattr(instance, 'debet_card'):
            DebetCard.objects.filter(expert=instance).update(**serializer.data)
        else:
            DebetCard.objects.create(expert_id=instance.id, **serializer.data)
        instance.preferred_payment_method = 1
        instance.save()
        debet_card = DebetCard.objects.get(expert_id=instance.id)
        return Response(DebetCardSerializer(debet_card).data, status=201)
    
    @action(["patch"], detail=True)
    def bank_transaction(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if hasattr(instance, 'bank_transaction'):
            BankTransaction.objects.filter(expert_id=instance.id).update(**serializer.data)
        else:
            BankTransaction.objects.create(expert_id=instance.id, **serializer.data)
        instance.preferred_payment_method = 2
        instance.save()
        bank_transaction = BankTransaction.objects.get(expert_id=instance.id)
        if not bank_transaction.scans.all().exists() or bank_transaction.scans.count() < 2:
            raise serializers.ValidationError({'scans':[_('Загрузите cканы уставных документов (ИНН, ОГРН)')]})
        return Response(BankTransactionSerializer(bank_transaction).data, status=201)
    
    
    @action(["patch"], detail=True)
    def verification(self, request, *args, **kwargs):
        errors={}
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if data['commercial_tours'] == 'no':
            data['commercial_tours_yearly'] = None
        if data['conflicts'] == 'no':
            data['conflicts_review'] = None
        if data['legal_restrictions'] == 'no':
            data['legal_restrictions_review'] = None
        if request.data.get('residency'):
            data['residency_id'] = request.data.get('residency')['id']
        if hasattr(instance, 'verifications'):
            VerificationRequest.objects.filter(expert_id=instance.id).update(**data)
        else:
            VerificationRequest.objects.create(expert_id=instance.id, **data)
        verification = VerificationRequest.objects.get(expert_id=instance.id)
        if request.data.get('tours_countries'):
            tours_countries = request.data.pop('tours_countries')
            ids = map(lambda tour_country: tour_country.get('id'), tours_countries)
            objects = TourMixin().get_mtm_objects(Country, ids)
            verification.tours_countries.set(objects)
        verification = VerificationRequest.objects.get(expert_id=instance.id)
        if not verification.residency:
            errors['residency'] = [_("Обязательное поле")]
        if not verification.tours_countries.all().exists():
            errors['tours_countries'] = [_("Обязательное поле")]
        if verification.commercial_tours == 'yes' and not verification.commercial_tours_yearly:
            errors['commercial_tours_yearly'] = [_("Обязательное поле")]
        if verification.conflicts == 'yes' and not verification.conflicts_review:
            errors['conflicts_review'] = [_("Обязательное поле")]
        if verification.legal_restrictions == 'yes' and not verification.legal_restrictions_review:
            errors['legal_restrictions_review'] = [_("Обязательное поле")]
        # if errors:
        #     raise ValidationError(errors)
        if errors or not instance.email_confirmed or not instance.phone_confirmed or (instance.preferred_payment_method == 2 and (not (hasattr(instance, 'bank_transaction') or not instance.bank_transaction.scans.all().exists() or instance.bank_transaction.scans.count() < 2)) or (instance.preferred_payment_method == 1 and not hasattr(instance, 'debet_card')) ):
            return Response({'error': True, 'message': _('Убедитесь, что у Вас заполнены все поля, подтверждены телефон и email, заполнены реквизиты для желаемого способа выплаты и загружены необходимые документы')}, status=403)
        return Response(VerificationRequestlSerializer(verification).data, status=201)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id']
    filterset_fields = ['first_name', 'last_name']

    def get_instance(self):
        return self.queryset.get(pk=self.request.user.id)

    @action(['get', 'put', 'patch', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):
        return get_me(self, request, *args, **kwargs)

    def get_queryset(self):
        qs = Customer.objects.all()
        return qs

    def get_serializer_class(self):
        is_staff = self.request.auth and self.request.user.is_staff
        if self.action in ['me', 'create', 'update', 'partial_update'] or (is_staff and self.action != 'list'):
            return CustomerMeSerializer
        return CustomerSerializer
    
    @action(['patch', 'delete'], detail=False)
    def avatar(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = AvatarSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
            customer = Customer.objects.get(pk=request.user.id)
            customer.avatar = data['avatar']
            customer.save()
        elif request.method == 'DELETE':
            customer = Customer.objects.get(pk=request.user.id)
            customer.avatar = None
            customer.save()
        return Response(CustomerMeSerializer(customer, context={'request':request}).data, status=status.HTTP_200_OK)
    

class TeamMemberViewSet(viewsets.ModelViewSet, TourMixin):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [TeamMemberPermission]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['expert',]

    def get_queryset(self):
        return super().get_queryset().filter(expert_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        instance = TeamMember.objects.create(expert_id = request.user.id, **data)
        return Response(TeamMemberSerializer(instance).data, status=201)
    
    def perform_update(self, serializer):
        if self.request.data.get('languages'):
            expert = self.get_object()
            self.set_languages(self.request, expert) 
        return super().perform_update(serializer)
    
    @action(['patch', 'delete'], detail=True)
    def avatar(self, request, *args, **kwargs):
        team_member = self.get_object()
        if request.method == 'PATCH':
            serializer = AvatarSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
            team_member.avatar = data['avatar']
            team_member.save()
        elif request.method == 'DELETE':
            team_member.avatar = None
            team_member.save()
        return Response(TeamMemberSerializer(team_member, context={'request':request}).data, status=status.HTTP_200_OK)