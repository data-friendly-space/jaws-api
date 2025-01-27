"""This module contains the workspace model"""
import uuid

from django.db import models


class Workspace(models.Model):
    """Model for the workspace"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_access_date = models.DateTimeField(null=True)
    facilitator = models.ForeignKey("user_management.User", on_delete=models.CASCADE,
                                    related_name="facilitated_workspaces")
    country = models.CharField(max_length=100)
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="organizations",
    )
    creator = models.ForeignKey('user_management.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'workspace'

    @classmethod
    def from_to(cls, workspace_to):
        """
        Creates a Workspace instance from a WorkspaceTO instance without saving it.

        Args:
            workspace_to (WorkspaceTO): Transfer Object containing the Workspace data.

        Returns:
            Workspace: An instance of the Workspace model.
        """
        from common.test_utils import User
        from user_management.contract.to.workspace_to import WorkspaceTO

        if workspace_to is None:
            return None

        if not isinstance(workspace_to, WorkspaceTO):
            raise ValueError("The argument must be an instance of WorkspaceTO")

        # Resolve ForeignKey relationships

        # Create the Workspace instance without saving
        workspace_instance = cls(
            id=uuid.UUID(workspace_to.id) if workspace_to.id else None,
            title=workspace_to.title,
            creation_date=workspace_to.creationDate,
            last_access_date=workspace_to.lastAccessDate,
            facilitator=User.from_to(workspace_to.facilitator),
            creator=User.from_to(workspace_to.creator),
            country=workspace_to.country,
        )

        return workspace_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]

    def set_analyses(self, workspace_to):
        """
        Sets the ManyToMany relationships for analyses in the Workspace instance.

        Args:
            workspace_to (WorkspaceTO): Transfer Object containing the Workspace data.
        """
        # Resolve ManyToMany relationships
        from analysis.models.analysis import Analysis
        analyses_instances = [Analysis.from_to(a) for a in workspace_to.analyses] if workspace_to.analyses else []

        # Set the analyses
        self.analyses.set(analyses_instances, clear=True)
