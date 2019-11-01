from django.shortcuts import render

# Create your views here.

# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json,time

def index2(request):
    return render(request, 'index2.html', {})

def room(request, room_name):
    u_name = request.COOKIES.get('user')
    t = time.strftime("%Y-%m-%d %X",time.localtime())
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),'user_name_jason':mark_safe(json.dumps(u_name)),'time':mark_safe(json.dumps(t+' '))})

