from django.urls import path
from . import views


urlpatterns = [
    path(
        "post_detail/<slug>/",
        views.PostDetailSerializerView.as_view(),
        name="post_detail",
    ),
    path(
        "createPost/<id>/",
        views.createPost,
        name="createPost",
    ),
    path(
        "editPost/",
        views.editPost,
        name="editPost",
    ),
    path(
        "getPostById/<id>/",
        views.getPostById,
        name="getPostById",
    ),
    path(
        "allpost/<id>/",
        views.getFriendPosts,
        name="allpost",
    ),
    path(
        "checkIfLiked/<id>/<post>/",
        views.checkIfLiked,
        name="checkIfLiked",
    ),
    path(
        "addLike/<id>/<post>/",
        views.addLike,
        name="addLike",
    ),
    path(
        "removeLike/<id>/<post>/",
        views.removeLike,
        name="removeLike",
    ),
    path(
        "addComment/<id>/<post>/",
        views.addComment,
        name="addComment",
    ),
]
