from django.urls import path

from . import views

urlpatterns = [
    path('support_tickets/', views.TicketListCreateRetrieveViewSet.as_view(), name='chat'),
]