from rest_framework import permissions


class TourPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'tour_set']:
            return request.auth and hasattr(request.user, 'expert')
        if view.action in ['aprove', 'decline']:
            return request.auth and request.user.is_staff
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy', 'propertyimages', 'gallary', 'dayimages', 'guestguideimages', 'tourcopy', 'wallpaper', 'planimages']:
            return request.auth and (obj.tour_basic.expert_id == request.user.id or request.user.is_staff)
        return True