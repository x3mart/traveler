# from rest_framework import permissions


# class BankDetailPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ['destroy',]:
#             return request.auth and request.user.is_staff
#         if view.action in ['update', 'partial_update']:
#             return request.auth and (hasattr(request.user, 'expert') or request.user.is_staff)
#         return True           

#     def has_object_permission(self, request, view, obj):
#         if view.action in ['update', 'partial_update',]:
#             return obj.expert.id == request.user.id or request.user.is_staff
#         return True