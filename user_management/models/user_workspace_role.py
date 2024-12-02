from django.db import models


class UserWorkspaceRole(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    workspace = models.ForeignKey('user_management.Workspace', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'workspace')

    def __str__(self):
        return f"{self.user} - {self.role} in {self.workspace}"

    class Meta:
        db_table = 'workspace_role'