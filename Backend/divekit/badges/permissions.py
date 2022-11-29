from rest_framework.permissions import BasePermission
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsStaffOrSelf(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view,obj):
        if request.user == obj or request.user.is_staff:
            return True
        return False