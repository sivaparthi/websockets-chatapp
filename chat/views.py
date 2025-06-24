
# Create your views here.
from .models import RoomUser
from django.shortcuts import render
from .models import Message
from django.http import JsonResponse

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return JsonResponse([
        {
            "username": m.username,
            "message": m.content,
            "timestamp": m.timestamp.isoformat()
        } for m in messages
    ], safe=False)

def active_users(request, room_name):
    users = RoomUser.objects.filter(room_name=room_name).values("username")
    return JsonResponse(list(users), safe=False)