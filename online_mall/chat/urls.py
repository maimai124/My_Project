# chat/urls.py
from django.urls import re_path

from chat.views import index2
from . import views

urlpatterns = [
    re_path('index2/',index2,name='index2'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
