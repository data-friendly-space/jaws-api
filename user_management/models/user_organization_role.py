from django.db import models


class UserOrganizationRole(models.Model):
    user = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('user_management.Organization', on_delete=models.CASCADE)
    role = models.ForeignKey('user_management.Role', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user} - {self.role} in {self.organization}"

    class Meta:
        db_table = 'organization_role'
