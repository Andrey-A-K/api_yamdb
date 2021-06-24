from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Role

User = get_user_model()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        )


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.is_staff or request.user.role == 'admin')


class ReviewCommentPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.is_authenticated()

        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author
                    or request.user.role == Role.ADMIN
                    or request.user.role == Role.MODERATOR)

        if request.method in SAFE_METHODS:
            return True
        return False
