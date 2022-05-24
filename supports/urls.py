from django.urls import path

from . import views

urlpatterns = [
    path('chats/', views.TicketListCreateRetrieveViewSet.as_view(), name='chat'),
]