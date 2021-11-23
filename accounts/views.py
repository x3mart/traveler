from django.db.models.aggregates import Avg
from accounts.permissions import ExpertPermission
from accounts.serializers import ExpertSerializer, UserSerializer
from rest_framework import viewsets
from accounts.models import Expert, User
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        return super().get_queryset()
    
class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [ExpertPermission]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['tours_count', 'tours_avg_rating']
    filterset_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = Expert.objects.annotate(tours_count=Count('tours'))
        return qs

