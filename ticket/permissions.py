from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_active:
            return True
        else:
            return request.user.is_staff


class IsAuthorizedOrUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_active:
            return True
        elif request.method in ['DELETE', 'PUT'] and request.user.is_superuser:
            return True

        else:
            if hasattr(request.user, 'is_authorized'):
                return request.user.is_authorized
            else:
                return False