from channels.generic.websocket import WebsocketConsumer

from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

import json

from channels.consumer import AsyncConsumer

from .models import Thread, Chat

from .serializers import ThreadSerializer, ChatSerializer
from auth_api.models import UserProfile

# from network.models import Connection


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.sender = self.scope["url_route"]["kwargs"]["sender_id"]
        self.receiver = self.scope["url_route"]["kwargs"]["receiver_id"]
        # Write check for connection

        self.thread_id = await self.get_thread(self.sender, self.receiver)
        print("self.thread_id", self.thread_id)
        self.chat_room = f"thread_{self.thread_id}"
        chat = await self.get_chat(self.thread_id)
        print("chat", chat)

        await self.channel_layer.group_add(self.chat_room, self.channel_name)

        await self.send(
            {
                "type": "websocket.accept",
            }
        )

        await self.send({"type": "websocket.send", "text": chat})

    async def websocket_receive(self, event):
        try:
            data = json.loads(event.get("text"))["text"]
            print("43", data)
            if data:
                recent_message = await self.create_chat(
                    self.sender, self.thread_id, data
                )
                await self.channel_layer.group_send(
                    self.chat_room,
                    {"type": "send_recent_message", "text": recent_message},
                )

            else:
                await self.send(
                    {
                        "type": "websocket.send",
                        "text": "No text containing message found.",
                    }
                )

        except:
            await self.send(
                {
                    "type": "websocket.send",
                    "text": "Error, kindly send data in right format.",
                }
            )

    async def websocket_disconnect(self, event):
        print("Disconnected :-<", event)

    @database_sync_to_async
    def get_chat(self, thread_id):
        chat = Thread.objects.get(id=thread_id).messages.all().order_by("time_created")
        sender = get_object_or_404(UserProfile, user=self.sender)
        serializer = ChatSerializer(chat, many=True, context={"sender": sender})
        return json.dumps({"messages": serializer.data})

    @database_sync_to_async
    def create_chat(self, sender_id, thread_id, text):
        sender = get_object_or_404(UserProfile, user=sender_id)
        serializer = ChatSerializer(
            data={"sender": sender.id, "thread": thread_id, "text": text},
            context={"sender": self.sender},
        )
        print("89", serializer)
        if serializer.is_valid():
            serializer.save()
            print("92", serializer.data)
            print("93", json.dumps(serializer.data))
            # return json.dumps({"messsage" : serializer.data})
            return json.dumps(serializer.data)
            # return text
        return serializer.errors

    @database_sync_to_async
    def get_thread(self, sender_id, receiver_id):
        sender = get_object_or_404(UserProfile, user=sender_id)
        receiver = get_object_or_404(UserProfile, user=receiver_id)
        thread = Thread.objects.filter(
            first_member=sender, second_member=receiver
        ) | Thread.objects.filter(first_member=receiver, second_member=sender)
        if thread.exists():
            return thread[0].id
        serializer = ThreadSerializer(
            data={"first_member": sender.id, "second_member": receiver.id}
        )
        if serializer.is_valid():
            serializer.save()
            return serializer.data["id"]
        return serializer.errors

    async def send_recent_message(self, event):
        print("116", event)
        await self.send({"type": "websocket.send", "text": event["text"]})
