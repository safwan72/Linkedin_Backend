from rest_framework import serializers

from . import models
from Profile.models import WorkExperience


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("email", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "email",
            "username",
            "id",
        )
        depth = 1


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    cover_pic = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        depth = 1

    def get_cover_pic(self, obj):
        request = self.context.get("request")
        try:
            cover_pic = obj.cover_pic.url
            return request.build_absolute_uri(cover_pic)
        except:
            return None

    def get_profile_pic(self, obj):
        request = self.context.get("request")
        try:
            profile_pic = obj.profile_pic.url
            return request.build_absolute_uri(profile_pic)
        except:
            return None


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = (
            "title",
            "company",
        )
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserProfileUpdateSerializer(
            instance.user, context={"request": self.context.get("request")}
        ).data
        return response


class UserProfileViewSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    cover_pic = serializers.SerializerMethodField()
    work = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.UserProfile
        exclude = (
            "first_name",
            "last_name",
            "id",
        )
        depth = 1

    def get_cover_pic(self, obj):
        request = self.context.get("request")
        cover_pic = obj.cover_pic.url
        return request.build_absolute_uri(cover_pic)

    def get_profile_pic(self, obj):
        request = self.context.get("request")
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)

    def get_work(self, obj):
        request = self.context.get("request")
        works = obj.workexperience.all()
        return UserWorkExperienceSerializer(
            works, context={"request": request}, many=True
        ).data
