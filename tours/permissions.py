from rest_framework import permissions


class TourPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create',]:
            return request.auth and hasattr(request.user, 'expert')
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.auth and (obj.expert_id == request.user.id or request.user.is_staff)
        return True

class TourTypePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.method in permissions.SAFE_METHODS:
            return True
        return request.auth and request.user.is_staff          


class TourDayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create',]:
            return request.auth and (request.user.is_staff or hasattr(request.user, 'expert'))
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.auth and (obj.tour.expert_id == request.user.id or request.user.is_staff)
        return True