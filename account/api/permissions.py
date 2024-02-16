from rest_framework.permissions import BasePermission

class CustomLoginPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_active and
            request.user.auth_token
        )
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and 
            request.user.is_active and
            request.user.auth_token
        )
    


class OrderedHasPermission(BasePermission):

    def has_permission(self, request, view):
        return super().has_permission(request, view)