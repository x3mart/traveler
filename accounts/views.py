from django.shortcuts import redirect
from rest_framework.decorators import action
from accounts.permissions import TeamMemberPermission, UserPermission, CustomerPermission, ExpertPermission
from accounts.serializers import AvatarSerializer, CustomerMeSerializer, EmailActivationSerializer, ExpertListSerializer, ExpertMeSerializer, ExpertSerializer, TeamMemberSerializer, UserSerializer, CustomerSerializer
from rest_framework import viewsets, status
from accounts.models import Expert, TeamMember, User, Customer
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
from djoser.compat import get_user_email
from djoser import utils
from djoser.conf import settings
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string
from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator


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
        context["url"] = settings.ACTIVATION_URL.format(**context)
        message_html = render_to_string("email_confirm.html", context)
        send_mail(subject, "message", 'x3mart@gmail.com', [self.user.email,], html_message=message_html,)


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
    
class ExpertViewSet(viewsets.ModelViewSet):
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
        return super().get_serializer_class()

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
        return Response(ExpertSerializer(expert, context={'request':request}).data, status=status.HTTP_200_OK)
    
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
        return super().get_serializer_class()

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [TeamMemberPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['expert',]

    def get_queryset(self):
        return super().get_queryset().filter(expert=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        data['expert_id'] = request.user.id
        instance = TeamMember.objects.create(**data)
        return Response(TeamMemberSerializer(instance).data, status=201)