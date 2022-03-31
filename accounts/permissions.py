from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth and request.user.is_staff 


class ExpertPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy',]:
            return request.auth and request.user.is_staff
        if view.action in ['me', 'update', 'partial_update', 'send_confirmation_email']:
            return request.auth
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['me', 'update', 'partial_update',]:
            return obj.id == request.user.id or request.user.is_staff
        return True


class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy',]:
            return request.auth and request.user.is_staff
        if view.action in ['me', 'update', 'partial_update',]:
            return request.auth
        return True           

    def has_object_permission(self, request, view, obj):
        if view.action in ['me', 'update', 'partial_update',]:
            return obj.id == request.user.id or request.user.is_staff
        return True


class TeamMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth and hasattr(request.user, 'expert')          

    def has_object_permission(self, request, view, obj):
        if view.action in ['destroy', 'update', 'partial_update',]:
            return obj.expert.id == request.user.id
        return True