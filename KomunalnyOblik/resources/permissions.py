from rest_framework import permissions
from .models import Role, CustomUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        ip_addr = request.META['REMOTE_ADDR']
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class Accountant(permissions.BasePermission):
    def has_permission(self, request, view):
        user_pk = CustomUser.objects.get(pk=request.user.pk)
        user_role = user_pk.role_id
        role = Role.objects.get(role_name='Accountant')
        role_id = role.id
        if user_role == role_id:
            return True
        else:
            return False


class Worker(permissions.BasePermission):
    def has_permission(self, request, view):
        user_pk = CustomUser.objects.get(pk=request.user.pk)
        user_role = user_pk.role_id
        role = Role.objects.get(role_name='Worker')
        role_id = role.id
        if user_role == role_id:
            return True
        else:
            return False