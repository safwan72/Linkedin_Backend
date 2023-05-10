from django.shortcuts import render
from . import serializers, models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from auth_api.permissions import isAuthorized
from auth_api.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from network.models import Connection
from rest_framework import mixins, viewsets, generics
import random
from rest_framework import status


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def createPost(request, id):
    data = request.data
    file = request.FILES
    if id:
        userProfile = UserProfile.objects.get(user=id)
        post = models.Post.objects.create(
            author=userProfile,
            post_title=data.get("post_title", ""),
            post_image=file.get("post_image", ""),
        )
        if post:
            return Response(True, status=status.HTTP_201_CREATED)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def editPost(request):
    data = request.data
    file = request.FILES
    id = data.get("id")
    post = data.get("post")
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        try:
            mypost = models.Post.objects.filter(author=userProfile, id=post)
            if mypost:
                mypost = mypost[0]
                mypost.post_title = data.get("post_title", "")
                mypost.post_image = file.get("post_image", "")
                mypost.save()

                post = models.Post.objects.get(author=userProfile, id=post)
                if post:
                    serializer = serializers.PostSerializers(
                        post, context={"request": request}
                    ).data
            return Response(serializer)
        except:
            return Response(False)


# Create your views here.
class PostDetailSerializerView(generics.RetrieveAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializers
    lookup_field = "slug"


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getPostById(request, id):
    post = models.Post.objects.get(id=id)
    if post:
        serializer = serializers.PostSerializers(
            post, context={"request": request}
        ).data
    return Response(serializer)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getFriendPosts(request, id):
    userProfile = UserProfile.objects.filter(user=id)
    posts = []
    if userProfile:
        userProfile = userProfile[0]
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_post = models.Post.objects.filter(author=friend.me).all()
                if all_post:
                    for post in all_post:
                        posts.append(post)

        mypost = userProfile.post_author.all()
        if mypost:
            for post in mypost:
                posts.append(post)
        random.shuffle(posts)
        serializer = serializers.PostSerializers(
            posts, context={"request": request}, many=True
        ).data
        return Response(serializer)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def checkIfLiked(request, id, post):
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        post = models.Post.objects.get(id=post)
        if userProfile:
            try:
                like_post = models.Like.objects.get(
                    liker=userProfile, post=post, liked=True
                )
                if like_post:
                    return Response(True)
            except:
                return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def addLike(request, id, post):
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        post = models.Post.objects.get(id=post)
        if userProfile:
            try:
                like_post, created = models.Like.objects.get_or_create(
                    liker=userProfile, post=post, liked=True
                )
                if like_post:
                    return Response(True)
            except:
                return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def removeLike(request, id, post):
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        post = models.Post.objects.get(id=post)
        if userProfile:
            like_post = models.Like.objects.get(
                liker=userProfile, post=post, liked=True
            )
            if like_post:
                like_post.delete()
            return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def addComment(request, id, post):
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        post = models.Post.objects.get(id=post)
        if userProfile:
            models.Comment.objects.create(
                commenter=userProfile, post=post, comment_text=request.data["comment"]
            )
            serializer = serializers.PostSerializers(
                post, context={"request": request}
            ).data
        return Response(serializer)
