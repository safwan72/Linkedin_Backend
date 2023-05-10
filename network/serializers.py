from rest_framework import serializers
from auth_api.serializers import UserProfileViewSerializer
from . import models


class ConnectionSerializer(serializers.ModelSerializer):
    sender = UserProfileViewSerializer()
    receiver = UserProfileViewSerializer()

    class Meta:
        model = models.Connection
        fields = "__all__"
        depth = 1
