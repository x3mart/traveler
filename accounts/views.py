from rest_framework.decorators import action
from accounts.permissions import UserPermission, CustomerPermission, ExpertPermission
from accounts.serializers import CustomerMeSerializer, ExpertListSerializer, ExpertMeSerializer, ExpertSerializer, UserSerializer, CustomerSerializer
from rest_framework import viewsets
from accounts.models import Expert, User, Customer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
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

    def get_instance(self):
        return self.queryset.get(pk=self.request.user.id)

    @action(['get', 'put', 'patch', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):
        return get_me(self, request, *args, **kwargs)

    def get_queryset(self):
        qs = Expert.objects.all()
        return qs
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExpertListSerializer
        is_staff = self.request.auth and self.request.user.is_staff
        if self.action == 'me' or is_staff:
            return ExpertMeSerializer
        return super().get_serializer_class()


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