from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from auth_api.permissions import isAuthorized
from auth_api.models import UserProfile, Followers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from network.models import Connection
from Profile.serializers import GetUserProfileSerializer
from . import models, serializers

# from network.ser import Connection
# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def getMyChatConnections(request, id):
    me = UserProfile.objects.get(user=id)
    myfriends = []
    connection2 = Connection.objects.filter(receiver=me, accepted=True)
    if connection2:
        for sender in connection2:
            myfriends.append(sender.sender)
    connection = Connection.objects.filter(sender=me, accepted=True)
    if connection:
        for receiver in connection:
            myfriends.append(receiver.receiver)

    # models.Connection.objects.filter(receiver=sender, accepted=True)
    serializer = GetUserProfileSerializer(
        myfriends, context={"request": request}, many=True
    ).data
    return Response(serializer)


@api_view(["GET"])
def GetChatList(request, sender, receiver):
    user1 = UserProfile.objects.get(user__id=sender)
    user2 = UserProfile.objects.get(user__id=receiver)
    try:
        threads = models.Thread.objects.filter(
            first_member=user1, second_member=user2
        ) | models.Thread.objects.filter(first_member=user2, second_member=user1)
    except:
        threads = []
    serializer = serializers.ChatListSerializer(
        threads, many=True, context={"request": request}
    )
    return Response(serializer.data)
