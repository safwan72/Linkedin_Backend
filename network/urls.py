from django.urls import path, include
from . import views

urlpatterns = [
    path("connect/", views.SendConnectionRequestView.as_view(), name="connect"),
    path(
        "check_connection/<sender>/<receiver>/",
        views.checkfollower,
        name="check_connection",
    ),
    path(
        "send_connection/",
        views.sendfollowrequest,
        name="send_connection",
    ),
    path(
        "getMyConnections/",
        views.getMyConnections,
        name="getMyConnections",
    ),
    path(
        "cancelfollowrequest/",
        views.cancelfollowrequest,
        name="cancelfollowrequest",
    ),
    path(
        "accept_connection/",
        views.acceptfollowrequest,
        name="accept_connection",
    ),
    path(
        "pendingReqs/<reciever>/",
        views.getPendingRequests,
        name="pendingReqs",
    ),
]
