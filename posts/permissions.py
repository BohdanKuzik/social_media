from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    - Allow everyone to access `list` and `retrieve` views.
    - All other actions require authentication.
    """
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(obj, "user") and obj.user == request.user
