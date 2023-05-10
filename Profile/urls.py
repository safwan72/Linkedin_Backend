from unicodedata import name
from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"headline", views.UserHeadLineView, basename="headline")

urlpatterns = [
    path(
        "contactinfo/<user__user__id>/",
        views.UserContactView.as_view(),
        name="contactinfo",
    ),
    path(
        "headline/<user__user__id>/", views.UserHeadLineView.as_view(), name="headline"
    ),
    path(
        "userabout/<user__user__id>/",
        views.UserAboutSectionView.as_view(),
        name="userabout",
    ),
    path(
        "userfeatured/<user__user__id>/",
        views.UserFeaturedSectionView.as_view(),
        name="userfeatured",
    ),
    path(
        "userwork/<user__user__id>/",
        views.UserWorkExperienceView.as_view(),
        name="userwork",
    ),
    path(
        "createworkexperience/",
        views.addUserWorkExperience,
        name="createuserwork",
    ),
    path(
        "createfeatured/",
        views.addUserFeatured,
        name="createfeatured",
    ),
    path(
        "useredu/<user__user__id>/", views.UserEducationView.as_view(), name="useredu"
    ),
    path(
        "userskill/<user__user__id>/", views.UserSkillView.as_view(), name="userskill"
    ),
    path("getUserByID/<id>/", views.getUserByID, name="getUserByID"),
    path("skills/", views.SkillSetView.as_view(), name="skills"),
]
