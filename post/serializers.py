from attr import fields
from rest_framework import serializers
from . import models
from auth_api.serializers import UserProfileUpdateSerializer, UserProfileSerializer
from auth_api.models import UserProfile


class PostSerializers(serializers.ModelSerializer):
    author = UserProfileUpdateSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="post_detail", read_only=True, lookup_field="slug"
    )

    class Meta:
        model = models.Post
        fields = "__all__"
        depth = 1

    def get_comments(self, obj):
        comments = obj.post_comment_post.all()
        return CommentSerializer(
            comments,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def get_comment_count(self, obj):
        return obj.post_comment_post.all().count()

    def get_like_count(self, obj):
        return obj.post_like_post.all().count()


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = "__all__"
