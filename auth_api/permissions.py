from rest_framework import permissions

from auth_api import views


class isAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
