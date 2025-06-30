import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message, RoomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)
        self.username = params.get("username", ["Anonymous"])[0]

        await self.add_user_to_room(self.room_name, self.username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_event",
                "event": f"{self.username} has joined the chat"
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list_update",
                "username": self.username,
                "action": "joined"
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.remove_user_from_room(self.room_name, self.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_event",
                "event": f"{self.username} has left the chat"
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list_update",
                "username": self.username,
                "action": "left"
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username", self.username)
        reply_to = data.get("reply_to")

        if message == "__typing__":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing",
                    "username": username
                }
            )
            return

        message_obj = await self.save_message(self.room_name, username, message, reply_to)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                'id': message_obj.id,
                "message": message,
                "username": username,
                "reply_to": reply_to
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "id": event["id"], 
            "message": event["message"],
            "username": event["username"],
            "reply_to": event.get("reply_to")
        }))

    async def user_list_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_update",
            "action": event["action"],
            "username": event["username"]
        }))

    async def user_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_event",
            "event": event["event"]
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))

    @sync_to_async
    def add_user_to_room(self, room_name, username):
        RoomUser.objects.get_or_create(room_name=room_name, username=username)

    @sync_to_async
    def remove_user_from_room(self, room_name, username):
        RoomUser.objects.filter(room_name=room_name, username=username).delete()

    @sync_to_async
    def save_message(self, room_name, username, message, reply_to=None):
        message = Message.objects.create(room_name=room_name, username=username, content=message, parent_data=reply_to)
        return message
