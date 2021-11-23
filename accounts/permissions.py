from rest_framework import permissions


class ExpertPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy',]:
            return request.auth and request.user.is_staff
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update',]:
            return obj.id == request.user.id or request.user.is_staff
        return True