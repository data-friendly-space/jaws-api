from django.db import models


class Workspace(models.Model):
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField()
    last_access_date = models.DateTimeField()
    facilitator = models.ForeignKey("user_management.User", on_delete=models.CASCADE,
                                    related_name="facilitated_workspaces")
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'workspace'
