from accounts.serializers import ExpertSerializer, UserSerializer
from rest_framework import viewsets
from accounts.models import Expert, User
from rest_framework.permissions import AllowAny
from modeltranslation.utils import get_language
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return super().get_queryset()
    
    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({"language": get_language()})
        return context
    
class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    def get_queryset(self):
        return super().get_queryset()
    
    def get_serializer_context(self):
        context = super(ExpertViewSet, self).get_serializer_context()
        context.update({"language": get_language()})
        return context
