from django.db import models

from user_management.models.affiliation import Affiliation
from user_management.models.ui_configuration import UiConfiguration
from user_management.models.organization import Organization
from user_management.models.position import Position
from user_management.models.user_workspace_role import UserWorkspaceRole
from user_management.models.workspace import Workspace


class User(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    profile_image = models.URLField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    ui_configuration = models.OneToOneField(UiConfiguration, on_delete=models.SET_NULL, null=True)
    workspaces = models.ManyToManyField(
        Workspace,
        through=UserWorkspaceRole,
        related_name='users'
    )

    def __str__(self):
        return f"{self.name} {self.lastname}"
