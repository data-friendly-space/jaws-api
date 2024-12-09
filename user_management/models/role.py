'''This module contains the role model'''
from django.db import models


class Role(models.Model):
    '''Role model'''
    role = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField('user_management.Permission', through="RolePermission")

    def __str__(self):
        return str(self.role)

    class Meta:
        db_table = 'role'


class RolePermission(models.Model):
    role = models.ForeignKey("user_management.Role", on_delete=models.CASCADE)
    permission = models.ForeignKey("user_management.Permission", on_delete=models.CASCADE)

    class Meta:
        db_table = 'role_permission'



