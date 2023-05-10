import json
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from . import models, serializers
from rest_framework import viewsets, generics, mixins, views
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from django.conf import settings
from oauth2_provider.models import get_access_token_model
from . import permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from network.models import Connection

# Create your views here.
class UserProfileSerializerView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.isAuthorized, IsAuthenticated]
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileUpdateSerializer
    lookup_field = "user__id"

    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            queryset = models.UserProfile.objects.get(user=kwargs["user__id"])
            if queryset:
                queryset.first_name = data.get("first_name", queryset.first_name)
                queryset.last_name = data.get("last_name", queryset.last_name)
                queryset.save()
            serializer = serializers.UserProfileUpdateSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)


class CheckToken(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try:
            token = get_access_token_model().objects.get(token=request.data["token"])
            if not token.is_expired():
                body = True
            else:
                body = False
        except:
            body = False
        body = json.dumps(body)
        return HttpResponse(body)


class GetUserFromToken(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try:
            token = get_access_token_model().objects.get(token=request.data["token"])
            # print(json.dumps(token.user.id))
            if token:
                body = {
                    "id": str(token.user.id),
                    "username": token.user.username,
                    "email": token.user.email,
                }
        except:
            body = {}
        body = json.dumps(body)
        return HttpResponse(body)


class UserCreateSerializerView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


def create(self, request, *args, **kwargs):
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([permissions.isAuthorized, IsAuthenticated])
def uploadProfilePic(request, format=None):
    user = models.UserProfile.objects.get(user=request.data["user"])
    if user:
        user.profile_pic = request.FILES["profile_pic"]
        user.save()
    serializer = serializers.UserProfileUpdateSerializer(
        user, context={"request": request}
    ).data
    return Response(serializer)


@api_view(["GET", "POST"])
@permission_classes([permissions.isAuthorized, IsAuthenticated])
def uploadCoverPic(request, format=None):
    user = models.UserProfile.objects.get(user=request.data["user"])
    if user:
        user.cover_pic = request.FILES["cover_pic"]
        user.save()
    serializer = serializers.UserProfileUpdateSerializer(
        user, context={"request": request}
    ).data
    return Response(serializer)


@api_view(["GET", "POST"])
@permission_classes([permissions.isAuthorized, IsAuthenticated])
def viewprofile(request, format=None):
    myProfile = models.UserProfile.objects.get(user=request.data["myProfile"])
    viewer = models.UserProfile.objects.get(user=request.data["viewer"])
    if myProfile and viewer:
        profileView = models.ProfileView.objects.get_or_create(
            myProfile=myProfile, viewer=viewer
        )
        if profileView:
            return Response(True)
        return Response(False)


@api_view(["GET"])
@permission_classes([permissions.isAuthorized, IsAuthenticated])
def profileViews(request, id):
    myProfile = models.UserProfile.objects.get(user=id)
    if myProfile:
        profileView = models.ProfileView.objects.filter(myProfile=myProfile).count()
        return Response(profileView)
    return Response(0)


@api_view(["GET", "POST"])
@permission_classes([permissions.isAuthorized, IsAuthenticated])
def getUsers(request, format=None):
    userprofile = models.UserProfile.objects.get(user=request.user)
    user = (
        models.UserProfile.objects.all()
        .exclude(user__is_superuser=True)
        .exclude(user=request.user)
    )
    allusers = []

    for iuser in user:
        allusers.append(iuser)
        case1 = Connection.objects.filter(sender=userprofile, accepted=True)
        case2 = Connection.objects.filter(receiver=userprofile, accepted=True)
        for obj in case1:
            if obj.receiver == iuser:
                allusers.remove(iuser)
        for obj in case2:
            if obj.sender == iuser:
                allusers.remove(iuser)
    serializer = serializers.UserProfileViewSerializer(
        allusers, context={"request": request}, many=True
    ).data
    return Response(serializer)
