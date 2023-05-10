from rest_framework import serializers
from . import models
from auth_api.serializers import UserProfileUpdateSerializer, UserProfileSerializer
from auth_api.models import UserProfile


class UserContactInfoSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.ContactInfo
        fields = "__all__"
        depth = 1


class UserHeadlineSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.Headline
        fields = "__all__"
        depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response["user"] = UserProfileUpdateSerializer(
    #         instance.user, context={"request": self.context.get("request")}
    #     ).data
    #     return response


class UserAboutSectionSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.AboutSection
        fields = "__all__"
        depth = 1


class UserFeaturedSectionSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.FeaturedSection
        fields = "__all__"
        depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response["user"] = UserProfileUpdateSerializer(
    #         instance.user, context={"request": self.context.get("request")}
    #     ).data
    #     return response

    def get_picture(self, obj):
        request = self.context.get("request")
        try:
            picture = obj.picture.url
            return request.build_absolute_uri(picture)
        except:
            return None


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.WorkExperience
        fields = "__all__"
        depth = 1


class UserEducationSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.Education
        fields = "__all__"
        depth = 1


class SkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SkillList
        fields = "__all__"
        depth = 1


class UserSkillSerializer(serializers.ModelSerializer):
    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.Skills
        fields = "__all__"
        depth = 1


class GetUserProfileSerializer(serializers.ModelSerializer):
    work = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    featured = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    headline = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()
    user = UserProfileSerializer(read_only=True)
    profile_pic = serializers.SerializerMethodField()
    cover_pic = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = "__all__"
        depth = 1

    def get_work(self, obj):
        request = self.context.get("request")
        works = obj.workexperience.all()
        return UserWorkExperienceSerializer(
            works, context={"request": request}, many=True
        ).data

    def get_about(self, obj):
        request = self.context.get("request")
        try:
            works = obj.myabout
        except:
            works = []
        return UserAboutSectionSerializer(works, context={"request": request}).data

    def get_headline(self, obj):
        request = self.context.get("request")
        try:
            works = obj.myheader
        except:
            works = []
        return UserHeadlineSerializer(works, context={"request": request}).data

    def get_contacts(self, obj):
        request = self.context.get("request")
        try:
            works = obj.contactme
        except:
            works = []
        return UserContactInfoSerializer(works, context={"request": request}).data

    def get_featured(self, obj):
        request = self.context.get("request")
        try:
            educations = obj.myfeatured
        except:
            educations = []
        return UserFeaturedSectionSerializer(
            educations, context={"request": request}
        ).data

    def get_education(self, obj):
        request = self.context.get("request")
        educations = obj.myeducation.all()
        return UserEducationSerializer(
            educations, context={"request": request}, many=True
        ).data

    def get_cover_pic(self, obj):
        request = self.context.get("request")
        cover_pic = obj.cover_pic.url
        return request.build_absolute_uri(cover_pic)

    def get_profile_pic(self, obj):
        request = self.context.get("request")
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)
