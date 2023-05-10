from django.dispatch import receiver
from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, views
from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from auth_api.permissions import isAuthorized
from auth_api.models import UserProfile, Followers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# from notification.models import Notifications

# Create your views here.
class SendConnectionRequestView(views.APIView):
    permission_classes = [isAuthorized, IsAuthenticated]

    def post(request, *args, **kwargs):
        pass


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def getMyConnections(request):
    sender = UserProfile.objects.get(user=request.data["sender"])
    connection = models.Connection.objects.filter(
        sender=sender, accepted=True
    ) | models.Connection.objects.filter(receiver=sender, accepted=True)
    serializer = serializers.ConnectionSerializer(
        connection, context={"request": request}, many=True
    ).data
    return Response(serializer)


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def checkfollower(request, sender, receiver):
    senderProfile = UserProfile.objects.get(user=sender)
    receiverProfile = UserProfile.objects.get(user=receiver)
    connection = models.Connection.objects.filter(
        sender=senderProfile, receiver=receiverProfile
    ) | models.Connection.objects.filter(sender=receiverProfile, receiver=senderProfile)
    if connection:
        connection = connection[0]
        if connection.accepted == True:
            return Response("accepted")
        elif connection.accepted == False and senderProfile == connection.sender:
            return Response("Sender pending")
        elif connection.accepted == False and senderProfile == connection.receiver:
            return Response("Receiver pending")
    else:
        return Response("not connected")


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def sendfollowrequest(request):
    sender = UserProfile.objects.get(user=request.data["sender"])
    receiver = UserProfile.objects.get(user=request.data["receiver"])
    connection = models.Connection.objects.get_or_create(
        sender=sender, receiver=receiver
    )
    # notification, created = Notifications.objects.get_or_create(
    #     target=receiver, source=sender, actions="Connection"
    # )
    if connection:
        connection = connection[0]
        if connection.accepted == True:
            return Response("accepted")
        elif connection.accepted == False and sender == connection.sender:
            return Response("Sender pending")
        elif connection.accepted == False and sender == connection.receiver:
            return Response("Receiver pending")
    else:
        return Response("not connected")


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def cancelfollowrequest(request):
    sender = UserProfile.objects.get(user=request.data["sender"])
    receiver = UserProfile.objects.get(user=request.data["receiver"])
    connection = models.Connection.objects.filter(
        sender=sender, receiver=receiver, accepted=False
    ) | models.Connection.objects.filter(
        sender=receiver, receiver=sender, accepted=False
    )
    if connection:
        connection = connection[0]
        connection.delete()
    return Response("not connected")


from rest_framework import status


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def acceptfollowrequest(request):
    sender = UserProfile.objects.get(user=request.data["sender"])
    receiver = UserProfile.objects.get(user=request.data["receiver"])
    connection = models.Connection.objects.filter(
        sender=sender, receiver=receiver, accepted=False
    )
    if connection:
        connection = connection[0]
        connection.accepted = True
        myfollowers, created = Followers.objects.get_or_create(me=sender)
        myfollowers1, created = Followers.objects.get_or_create(me=receiver)
        myfollowers.myfollowers.add(receiver)
        myfollowers1.myfollowers.add(sender)
        myfollowers.save()
        myfollowers1.save()
        connection.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # connection = models.Connection.objects.filter(receiver=receiver, accepted=False)
    # serializer = serializers.ConnectionSerializer(
    #     connection, context={"request": request}, many=True
    # ).data


@api_view(["GET"])
@permission_classes([isAuthorized, IsAuthenticated])
def getPendingRequests(request, reciever):
    receiver = UserProfile.objects.get(user=reciever)
    connection = models.Connection.objects.filter(receiver=receiver, accepted=False)
    serializer = serializers.ConnectionSerializer(
        connection, context={"request": request}, many=True
    ).data
    return Response(serializer)
