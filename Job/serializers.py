from rest_framework import serializers
from . import models
from auth_api.serializers import UserProfileUpdateSerializer


class CompanyAboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyAboutSection
        fields = "__all__"
        depth = 1


class CompanyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyJobs
        fields = "__all__"
        depth = 1


class SavedJobSerializer(serializers.ModelSerializer):
    job = CompanyJobSerializer()
    me = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.SavedJobs
        fields = "__all__"
        depth = 1


class CompanySerializer(serializers.ModelSerializer):
    created_by = UserProfileUpdateSerializer(read_only=True)
    logo = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    job_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    jobs = serializers.SerializerMethodField()

    class Meta:
        model = models.Company
        fields = "__all__"

    def get_jobs(self, obj):
        jobs = obj.company_job_post.all()
        return CompanyJobSerializer(
            jobs,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def get_posts(self, obj):
        posts = obj.mycompanypost.all()
        return CompanyPostSerializer(
            posts,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def get_job_count(self, obj):
        return obj.company_job_post.all().count()

    def get_post_count(self, obj):
        return obj.mycompanypost.all().count()

    def get_follower_count(self, obj):
        return obj.followers_of_myCompanny.all()[0].myfollowers.count()

    def get_cover_photo(self, obj):
        request = self.context.get("request")
        try:
            cover_photo = obj.cover_photo.url
            return request.build_absolute_uri(cover_photo)
        except:
            return None

    def get_logo(self, obj):
        request = self.context.get("request")
        try:
            logo = obj.logo.url
            return request.build_absolute_uri(logo)
        except:
            return None

    def get_about(self, obj):
        try:
            about = obj.mycompanyabout
        except:
            about = []
        return CompanyAboutSectionSerializer(
            about,
            context={"request": self.context.get("request")},
        ).data


class CompanyPostSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = models.CompanyPost
        fields = "__all__"
        depth = 1

    def get_photo(self, obj):
        request = self.context.get("request")
        try:
            photo = obj.photo.url
            return request.build_absolute_uri(photo)
        except:
            return None

    def get_comments(self, obj):
        comments = obj.company_post_comment_post.all()
        return CompanyPostCommentSerializer(
            comments,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def get_comment_count(self, obj):
        return obj.company_post_comment_post.all().count()

    def get_like_count(self, obj):
        return obj.company_post_post_like.all().count()


class CompanyPostCommentSerializer(serializers.ModelSerializer):
    commenter = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = models.CompanyPostComment
        fields = "__all__"
