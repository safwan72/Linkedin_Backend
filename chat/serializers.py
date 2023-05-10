from rest_framework import serializers
from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["sender"] = instance.sender.user.username
        response["is_my_msg"] = (
            True if instance.sender.id == self.context.get("sender") else False
        )
        response["sender_id"] = instance.sender.id
        return response


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     if not self.context.get("request").user == instance.first_member:
    #         response["user_id"] = instance.first_member.id
    #         response["user_name"] = instance.first_member.user.username
    #         try:
    #             response["text"] = instance.messages.first().text
    #         except:
    #             response["text"] = None
    #     else:
    #         response["user_id"] = instance.second_member.id
    #         response["user_name"] = instance.second_member.user.username
    #         try:
    #             response["text"] = instance.messages.first().text
    #         except:
    #             response["text"] = None
    #     return response
