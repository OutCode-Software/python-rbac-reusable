from django.db import IntegrityError, models
from .user_auth import User

from ..permissons import PERMISSIONS


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100)


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as _:
            pass

    # @property
    # def permissions(self):
    #     try:
    #         return [rp.permission for rp in self.role_permissions.all()]
    #     except RolePermission.DoesNotExist as _:
    #         return []

    @property
    def users(self):
        return [role_user.user for role_user in self.role_users.all()]


class RolePermission(models.Model):
    role = models.ForeignKey(Role, related_name='role_permissions', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, related_name='permission_role', on_delete=models.CASCADE)


class UserRole(models.Model):
    user = models.ForeignKey(User, related_name='user_role', on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, related_name='role_users', on_delete=models.SET_NULL, null=True)

    @property
    def permissions(self):
        return self.role.role_permissions
