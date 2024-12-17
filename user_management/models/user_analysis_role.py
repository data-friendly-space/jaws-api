from django.db import models


class UserAnalysisRole(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    analysis = models.ForeignKey('user_management.Analysis', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'analysis')

    def __str__(self):
        return f"{self.user} - {self.role} in {self.analysis}"

    class Meta:
        db_table = 'workspace_role'
