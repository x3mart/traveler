from django.urls import path
from .views import tg_update_handler


urlpatterns = [
    path('5365298811:AAFnY6zwIKcG4Rd8gP5azbJL4nzmwlEgVkk/', tg_update_handler, name='tg_update'),
]