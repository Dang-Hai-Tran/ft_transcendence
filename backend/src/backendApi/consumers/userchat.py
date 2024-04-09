from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from ..models import User, UserMessage, ChannelMessage


# Implement the chat consumer between two users
class UserChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, user_id: int, other_user_id: int):
        self.user_id = user_id
        self.other_user_id = other_user_id
        self.room_name = f"userchat_{self.user_id}_{self.other_user_id}"

        # Join the room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = text_data["message"]
        # Create a new message in the database
        sender = await self.get_user(self.user_id)
        receiver = await self.get_user(self.other_user_id)
        new_message = await self.create_message(sender, receiver, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user_id,
                "receiver_id": self.other_user_id,
            },
        )

    async def get_user(self, user_id):
        return await User.objects.aget(id=user_id)

    async def create_message(self, sender, receiver, content):
        return await UserMessage.objects.acreate(
            sender=sender, receiver=receiver, content=content
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        receiver_id = event["receiver_id"]
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender_id": sender_id, "receiver_id": receiver_id}
            )
        )
