from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"company", views.CompanySerializerView, basename="company")

urlpatterns = [
    path("createMyCompany/<id>/", views.createMyCompany, name="createMyCompany"),
    path(
        "getCompanyPostByID/<id>/", views.getCompanyPostByID, name="getCompanyPostByID"
    ),
    path(
        "getFollowedCompanyPosts/<id>/",
        views.getFollowedCompanyPosts,
        name="getFollowedCompanyPosts",
    ),
    path(
        "checkLikedCompanyPost/<id>/<post>/",
        views.checkLikedCompanyPost,
        name="checkLikedCompanyPost",
    ),
    path(
        "checkifFollowedCompany/<id>/<company>/",
        views.checkifFollowedCompany,
        name="checkifFollowedCompany",
    ),
    path(
        "createJobPost/<company>/",
        views.createJobPost,
        name="createJobPost",
    ),
    path(
        "getPageAuthorizedByUser/<id>/<page>/",
        views.getPageAuthorizedByUser,
        name="getPageAuthorizedByUser",
    ),
    path(
        "checkAppliedStatus/<id>/<company>/<jobId>/",
        views.checkAppliedStatus,
        name="checkAppliedStatus",
    ),
    path(
        "checkSaveStatus/<id>/<jobId>/",
        views.checkSaveStatus,
        name="checkSaveStatus",
    ),
    path(
        "applytoJob/",
        views.applytoJob,
        name="applytoJob",
    ),
    path(
        "cancelApplyJob/",
        views.cancelApplyJob,
        name="cancelApplyJob",
    ),
    path(
        "recentJobs/",
        views.recentJobs,
        name="recentJobs",
    ),
    path(
        "followCompany/",
        views.followCompany,
        name="followCompany",
    ),
    path(
        "likeCompanyPost/",
        views.likeCompanyPost,
        name="likeCompanyPost",
    ),
    path(
        "unfollowCompany/",
        views.unfollowCompany,
        name="unfollowCompany",
    ),
    path(
        "unlikeCompanyPost/",
        views.unlikeCompanyPost,
        name="unlikeCompanyPost",
    ),
    path(
        "addComment/<id>/<post>/",
        views.addComment,
        name="addComment",
    ),
    path(
        "saveJob/",
        views.saveJob,
        name="saveJob",
    ),
    path(
        "cancelSaveJob/",
        views.cancelSaveJob,
        name="cancelSaveJob",
    ),
    path(
        "getSavedJobs/<id>/",
        views.getSavedJobs,
        name="getSavedJobs",
    ),
] + router.urls
