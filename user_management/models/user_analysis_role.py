from django.db import models


class UserAnalysisRole(models.Model):
    user = models.ForeignKey('User')
    analysis = models.ForeignKey('user_management.Analysis')
    role = models.ForeignKey('Role')

    class Meta:
        unique_together = ('user', 'analysis')

    def __str__(self):
        return f"{self.user} - {self.role} in {self.analysis}"

    class Meta:
        db_table = 'workspace_role'
