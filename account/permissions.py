from rest_framework.permissions import BasePermission

class IsAuthorPermission(BasePermission):
    def has_permission(self, request, view, obj):
        return bool(
            request.user == obj.user
        )
