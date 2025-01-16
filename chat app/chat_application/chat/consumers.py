# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = f'chat_{self.user.id}'
        self.room_group_name = f'chat_{self.user.id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        to_user_id = data['to_user_id']
        message = data['message']

        to_user = User.objects.get(id=to_user_id)
        Message.objects.create(from_user=self.user, to_user=to_user, content=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'from_user': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        from_user = event['from_user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'from_user': from_user,
        }))
