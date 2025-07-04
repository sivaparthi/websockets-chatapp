from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("messages/<str:room_name>/", views.get_messages, name="get_messages"),
    path("users/<str:room_name>/", views.active_users)
]