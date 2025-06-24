from django.db import models

class Message(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class RoomUser(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room_name', 'username')