from django.urls import path

from . import views

urlpatterns = [
    path('chats/', views.UserChatListCreateView.as_view(), name='chat'),
    path('chats/<str:room_name>/', views.room, name='room'),
    path('notification/', views.room2, name='room'),
]