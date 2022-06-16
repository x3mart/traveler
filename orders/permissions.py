from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy',]:
            return request.auth and request.user.is_staff
        if view.action in ['create', 'update', 'partial_update',]:
            return request.auth and (request.user.is_staff or hasattr(request.user, 'customer'))
        return request.auth           

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'ask_confirmation', 'book', 'remove']:
            return obj.customer_id == request.user.id or request.user.is_staff
        if view.action in ['aprove', 'decline']:
            return obj.expert_id == request.user.id or request.user.is_staff
        if view.action in ['cancel', 'retrieve']:
            return obj.expert_id == request.user.id or obj.expert_id == request.user.id or request.user.is_staff
        return True