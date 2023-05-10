from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, views
from rest_framework.permissions import IsAuthenticated
from auth_api.permissions import isAuthorized
from auth_api.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from . import models, serializers
from rest_framework import status
import random

# Create your views here.
class CompanySerializerView(viewsets.ViewSet):
    # permission_classes = [isAuthorized, IsAuthenticated]

    def list(self, request):
        queryset = models.Company.objects.all()
        serializer = serializers.CompanySerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = serializers.CompanySerializer(
            company, context={"request": request}
        )
        return Response(serializer.data)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def createMyCompany(request, id):
    data = request.data
    file = request.FILES
    if id:
        userProfile = UserProfile.objects.get(user=id)
        company = models.Company.objects.create(
            created_by=userProfile,
            name=data.get("name", ""),
            headline=data.get("headline", ""),
            logo=file.get("logo", ""),
            cover_photo=file.get("cover_photo", ""),
        )
        if company:
            companyAbout = models.CompanyAboutSection.objects.get_or_create(
                company=company,
                description=data.get("description", ""),
                size=data.get("size", ""),
                type=data.get("type", ""),
                industry=data.get("industry", ""),
                phone=data.get("phone", ""),
                location=data.get("location", ""),
                website=data.get("website", ""),
                founded=data.get("founded", ""),
            )
            if companyAbout:
                id = company.id
                return Response(
                    {"created": True, "id": id}, status=status.HTTP_201_CREATED
                )
            return Response(False, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def checkLikedCompanyPost(request, id, post):
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        companyPosts = models.CompanyPost.objects.get(id=post)
        if userProfile and companyPosts:
            try:
                likeStatus = models.CompanyPostLike.objects.filter(
                    liker=userProfile, post=companyPosts, liked=True
                )
                if likeStatus:
                    return Response(True)
            except:
                return Response(False)
    return Response(False)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def checkifFollowedCompany(request, id, company):
    if id and company:
        userProfile = UserProfile.objects.get(user=id)
        myCompany = models.Company.objects.get(id=company)
        if userProfile and myCompany:
            followerList = models.CompanyFollowers.objects.filter(company=myCompany)
            if followerList:
                followerList = followerList[0]
                # print(follow)
                for follow in followerList.myfollowers.all():
                    if follow == userProfile:
                        return Response(True)
                return Response(False)


@api_view(
    [
        "POST",
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def followCompany(request):
    id = request.data["id"]
    company = request.data["company"]
    if id and company:
        userProfile = UserProfile.objects.get(user=id)
        myCompany = models.Company.objects.get(id=company)
        if userProfile and myCompany:
            followerList = models.CompanyFollowers.objects.filter(company=myCompany)
            if followerList:
                followerList = followerList[0]
                # print(follow)
                followerList.myfollowers.add(userProfile)
                followerList.save()
                for follow in followerList.myfollowers.all():
                    if follow == userProfile:
                        return Response(True)
                return Response(False)


@api_view(
    [
        "POST",
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def unfollowCompany(request):
    id = request.data["id"]
    company = request.data["company"]
    if id and company:
        userProfile = UserProfile.objects.get(user=id)
        myCompany = models.Company.objects.get(id=company)
        if userProfile and myCompany:
            followerList = models.CompanyFollowers.objects.filter(company=myCompany)
            if followerList:
                followerList = followerList[0]
                followerList.myfollowers.remove(userProfile)
                followerList.save()
                for follow in followerList.myfollowers.all():
                    if follow == userProfile:
                        return Response(True)
                return Response(False)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getFollowedCompanyPosts(request, id):
    userProfile = UserProfile.objects.filter(user=id)
    posts = []
    if userProfile:
        userProfile = userProfile[0]
        companies = models.Company.objects.all()
        # 1. Loop through all companies
        # 2. Loop through followers of all companies
        # 3. While looping through followers if any follower matches the userprofile then for the post of that company store all the posts of that company into a temporary array and then shuffle the array and serialize the posts.
        for company in companies:
            for Allfollowers in company.followers_of_myCompanny.all():
                for follower in Allfollowers.myfollowers.all():
                    if follower == userProfile:
                        for post in company.mycompanypost.all():
                            posts.append(post)
                        random.shuffle(posts)
        serializer = serializers.CompanyPostSerializer(
            posts, context={"request": request}, many=True
        ).data
        return Response(serializer)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getCompanyPostByID(request, id):
    post = models.CompanyPost.objects.get(id=id)
    if post:
        serializer = serializers.CompanyPostSerializer(
            post, context={"request": request}
        ).data
    return Response(serializer)


@api_view(
    [
        "POST",
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def likeCompanyPost(request):
    id = request.data["id"]
    post = request.data["post"]
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        companyPost = models.CompanyPost.objects.get(id=post)
        if userProfile and companyPost:
            createLikePost = models.CompanyPostLike.objects.get_or_create(
                liker=userProfile, post=companyPost
            )
            if createLikePost:
                return Response(True)
        return Response(False)


@api_view(
    [
        "POST",
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def unlikeCompanyPost(request):
    id = request.data["id"]
    post = request.data["post"]
    if id and post:
        userProfile = UserProfile.objects.get(user=id)
        companyPost = models.CompanyPost.objects.get(id=post)
        if userProfile and companyPost:
            createLikePost = models.CompanyPostLike.objects.get(
                liker=userProfile, post=companyPost, liked=True
            )
            if createLikePost:
                createLikePost.delete()
                createLikePost.save()
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
        post = models.CompanyPost.objects.get(id=post)
        if userProfile:
            models.CompanyPostComment.objects.create(
                commenter=userProfile, post=post, comment_text=request.data["comment"]
            )
            serializer = serializers.CompanyPostSerializer(
                post, context={"request": request}
            ).data
        return Response(serializer)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getPageAuthorizedByUser(request, id, page):
    userProfile = UserProfile.objects.get(user=id)
    try:
        page = models.Company.objects.get(id=page, created_by=userProfile)
        if page:
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
def createJobPost(request, company):
    data = request.data
    if company:
        myCompany = models.Company.objects.get(id=company)
        createcompany = models.CompanyJobs.objects.create(
            posted_by=myCompany,
            job_title=data.get("job_title", ""),
            job_description=data.get("job_description", ""),
            isOpen=True,
        )
        if createcompany:
            queryset = models.Company.objects.all()
            company = get_object_or_404(queryset, pk=company)
            serializer = serializers.CompanySerializer(
                company, context={"request": request}
            )
        return Response(serializer.data)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def recentJobs(request):
    jobs = models.CompanyJobs.objects.all().filter(isOpen=True)
    if jobs:
        serializer = serializers.CompanyJobSerializer(
            jobs, context={"request": request}, many=True
        )
    return Response(serializer.data)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def applytoJob(request):
    data = request.data
    myId = data.get("id")
    company = data.get("company")
    jobId = data.get("job")
    userProfile = UserProfile.objects.get(user=myId)
    try:
        company = models.Company.objects.get(id=company)
        jobs = models.CompanyJobs.objects.filter(
            posted_by=company, isOpen=True, id=jobId
        )
        if jobs:
            jobs = jobs[0]
            jobs.applied.add(userProfile)
            jobs.save()
            return Response(True)
        return Response(False)
    except:
        return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def checkAppliedStatus(request, id, company, jobId):
    userProfile = UserProfile.objects.get(user=id)
    try:
        company = models.Company.objects.get(id=company)
        jobs = models.CompanyJobs.objects.filter(
            posted_by=company, isOpen=True, id=jobId
        )
        if jobs:
            jobs = jobs[0]
            for appliers in jobs.applied.all():
                if appliers == userProfile:
                    return Response(True)
        return Response(False)
    except:
        return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def cancelApplyJob(request):
    data = request.data
    myId = data.get("id")
    company = data.get("company")
    jobId = data.get("job")
    userProfile = UserProfile.objects.get(user=myId)
    try:
        company = models.Company.objects.get(id=company)
        jobs = models.CompanyJobs.objects.filter(
            posted_by=company, isOpen=True, id=jobId
        )
        if jobs:
            jobs = jobs[0]
            jobs.applied.remove(userProfile)
            jobs.save()
            return Response(False)
        return Response(False)
    except:
        return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def saveJob(request):
    data = request.data
    myId = data.get("id")
    job = data.get("job")
    userProfile = UserProfile.objects.get(user=myId)
    myJob = models.CompanyJobs.objects.get(id=job)
    try:
        savejob = models.SavedJobs.objects.create(me=userProfile, job=myJob)
        if savejob:
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
def checkSaveStatus(request, id, jobId):
    userProfile = UserProfile.objects.get(user=id)
    try:
        jobs = models.CompanyJobs.objects.get(isOpen=True, id=jobId)
        savedJob = models.SavedJobs.objects.filter(job=jobs, me=userProfile)
        if savedJob:
            savedJob = savedJob[0]
            return Response(True)
        else:
            return Response(False)
    except:
        return Response(False)


@api_view(
    [
        "GET",
        "POST",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def cancelSaveJob(request):
    data = request.data
    myId = data.get("id")
    job = data.get("job")
    userProfile = UserProfile.objects.get(user=myId)
    myJob = models.CompanyJobs.objects.get(id=job)
    savedjob = models.SavedJobs.objects.get(me=userProfile, job=myJob)
    if savedjob:
        savedjob.delete()
        return Response(False)
    else:
        return Response(False)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([isAuthorized, IsAuthenticated])
def getSavedJobs(request, id):
    userProfile = UserProfile.objects.get(user=id)
    jobs = models.SavedJobs.objects.filter(me=userProfile).all()
    if jobs:
        jobs = jobs
    else:
        jobs = []

    serializer = serializers.SavedJobSerializer(
        jobs, context={"request": request}, many=True
    ).data
    return Response(serializer)
