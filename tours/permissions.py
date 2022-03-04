from rest_framework import permissions


class TourPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create',]:
            return request.auth and hasattr(request.user, 'expert')
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy', 'propertyimages', 'gallary', 'dayimages', 'guestguideimages', 'tourcopy']:
            return request.auth and (obj.tour_basic.expert_id == request.user.id)
        return True