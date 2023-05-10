from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, views
from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from auth_api.permissions import isAuthorized
from auth_api.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
class SkillSetView(generics.ListAPIView):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.SkillList.objects.all()
    serializer_class = serializers.SkillSetSerializer


class UserSkillView(generics.RetrieveAPIView, mixins.CreateModelMixin):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.Skills.objects.all()
    serializer_class = serializers.UserSkillSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset = models.Skills.objects.filter(user=user)
            serializer = serializers.UserSkillSerializer(
                queryset, context={"request": request}, many=True
            ).data
        except:
            serializer = []
        return Response(serializer)

    def post(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        skill = get_object_or_404(models.SkillList, skill=request.data["skill"])
        queryset, created = models.Skills.objects.get_or_create(
            user=user, skill=skill, top_skill=request.data["top_skill"]
        )
        try:
            queryset = models.Skills.objects.filter(user=user)
            serializer = serializers.UserSkillSerializer(
                queryset, context={"request": request}, many=True
            ).data
        except:
            serializer = []
        return Response(serializer)


class UserContactView(generics.RetrieveUpdateAPIView):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.ContactInfo.objects.all()
    serializer_class = serializers.UserContactInfoSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset = models.ContactInfo.objects.get(user=user)
            serializer = serializers.UserContactInfoSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)

    def patch(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        data = request.data
        queryset, created = models.ContactInfo.objects.get_or_create(user=user)
        if queryset:
            queryset.user = user
            queryset.website = data.get("website", queryset.website)
            queryset.phone = data.get("phone", queryset.phone)
            queryset.address = data.get("address", queryset.address)
            queryset.birthday = data.get("birthday", queryset.birthday)
            queryset.save()
        serializer = serializers.UserContactInfoSerializer(
            queryset, context={"request": request}
        ).data
        return Response(serializer)


class UserHeadLineView(generics.RetrieveUpdateAPIView, mixins.CreateModelMixin):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.Headline.objects.all()
    serializer_class = serializers.UserHeadlineSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset = models.Headline.objects.get(user=user)
            serializer = serializers.UserHeadlineSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, user=kwargs["user__user__id"])
        data = request.data
        try:
            queryset = models.Headline.objects.get(user=user)
            if queryset:
                queryset.header = data.get("header", queryset.header)
                queryset.save()
            serializer = serializers.UserHeadlineSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, user=kwargs["user__user__id"])
        data = request.data
        try:
            queryset = models.Headline.objects.create(user=user)
            if queryset:
                queryset.header = data.get("header", queryset.header)
                queryset.save()
            serializer = serializers.UserHeadlineSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)


class UserAboutSectionView(generics.RetrieveUpdateAPIView):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.AboutSection.objects.all()
    serializer_class = serializers.UserAboutSectionSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset = models.AboutSection.objects.get(user=user)
            serializer = serializers.UserAboutSectionSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)

    def patch(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset, created = models.AboutSection.objects.get_or_create(user=user)
            if queryset:
                queryset.description = request.data.get("description")
                queryset.save()
            serializer = serializers.UserAboutSectionSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)


# @api_view(["GET", "POST"])
# @permission_classes([isAuthorized, IsAuthenticated])
# def addUserAbout(request, format=None):
#     user = get_object_or_404(UserProfile, user=request.data["user"])
#     data = request.data
#     models.FeaturedSection.objects.create(
#         user=user,
#         title=data.get("title", ""),
#         description=data.get("description", ""),
#         link=data.get("link", ""),
#         picture=request.FILES["picture"],
#     )
#     queryset = models.FeaturedSection.objects.get(user=user)
#     serializer = serializers.UserFeaturedSectionSerializer(
#         queryset, context={"request": request}
#     ).data
#     return Response(serializer)


class UserFeaturedSectionView(generics.RetrieveUpdateAPIView):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.FeaturedSection.objects.all()
    serializer_class = serializers.UserFeaturedSectionSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        try:
            queryset = models.FeaturedSection.objects.get(user=user)
            serializer = serializers.UserFeaturedSectionSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, user=kwargs["user__user__id"])
        queryset = models.FeaturedSection.objects.get(user=user)
        data = request.data
        try:
            queryset = models.FeaturedSection.objects.get(user=user)
            if queryset:
                queryset.description = data.get("description", queryset.description)
                queryset.picture = request.FILES.get("picture", queryset.picture)
                queryset.title = data.get("title", queryset.title)
                queryset.link = data.get("link", queryset.link)
                queryset.save()
            serializer = serializers.UserFeaturedSectionSerializer(
                queryset, context={"request": request}
            ).data
        except:
            serializer = []
        return Response(serializer)


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def addUserFeatured(request, format=None):
    user = get_object_or_404(UserProfile, user=request.data["user"])
    data = request.data
    models.FeaturedSection.objects.create(
        user=user,
        title=data.get("title", ""),
        description=data.get("description", ""),
        link=data.get("link", ""),
        picture=request.FILES["picture"],
    )
    queryset = models.FeaturedSection.objects.get(user=user)
    serializer = serializers.UserFeaturedSectionSerializer(
        queryset, context={"request": request}
    ).data
    return Response(serializer)


class UserWorkExperienceView(generics.RetrieveUpdateAPIView, mixins.CreateModelMixin):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.WorkExperience.objects.all()
    serializer_class = serializers.UserWorkExperienceSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        queryset = models.WorkExperience.objects.filter(user=user)
        serializer = serializers.UserWorkExperienceSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([isAuthorized, IsAuthenticated])
def addUserWorkExperience(request, format=None):
    user = get_object_or_404(UserProfile, user=request.data["user"])
    models.WorkExperience.objects.create(
        user=user,
        title=request.data["title"],
        company=request.data["company"],
        location=request.data["location"],
        start_date=request.data["start_date"],
        end_date=request.data["end_date"],
        description=request.data["description"],
        currently_working=request.data["currently_working"],
        employment_type=request.data["employment_type"],
    )
    queryset = models.WorkExperience.objects.filter(user=user)
    serializer = serializers.UserWorkExperienceSerializer(
        queryset, many=True, context={"request": request}
    )
    return Response(serializer.data)


class UserEducationView(generics.RetrieveUpdateAPIView, mixins.CreateModelMixin):
    permission_classes = [isAuthorized, IsAuthenticated]
    queryset = models.Education.objects.all()
    serializer_class = serializers.UserEducationSerializer
    lookup_field = "user__user__id"

    def retrieve(self, request, user__user__id):
        user = get_object_or_404(UserProfile, user=user__user__id)
        queryset = models.Education.objects.filter(user=user)
        serializer = serializers.UserEducationSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, user=kwargs["user__user__id"])
        data = request.data
        models.Education.objects.create(
            user=user,
            school=data.get("school", ""),
            degree=data.get("degree", ""),
            grade=data.get("grade", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            description=data.get("description", ""),
            activities=data.get("activities", ""),
            field_of_study=data.get("field_of_study", ""),
            currently_studying=data.get("currently_studying", ""),
        )
        queryset = models.Education.objects.filter(user=user)
        serializer = serializers.UserEducationSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserByID(request, id):
    user = get_object_or_404(UserProfile, user=id)
    serializer = serializers.GetUserProfileSerializer(
        user, context={"request": request}
    )
    return Response(serializer.data)
