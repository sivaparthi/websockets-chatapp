
# Create your views here.
from django.shortcuts import render
from .models import Message
from django.http import JsonResponse

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')[:50]
    return JsonResponse([
        {"username": m.username, "message": m.content} for m in messages
    ], safe=False)