from django.urls import path
from . import views


urlpatterns = [
    path(
        "getMyChatConnections/<id>/",
        views.getMyChatConnections,
        name="getMyChatConnections",
    ),
    path("history/<sender>/<receiver>/", views.GetChatList),
]
