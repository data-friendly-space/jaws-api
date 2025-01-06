"""This module contains the notification model"""
from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    """Notification model"""
    user = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    read = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=[('info', 'Info'), ('alert', 'Alert'), ('warning', 'Warning')])

    def __str__(self):
        """Table's metadata"""
        return f"Notification for {self.user.username} - {self.type}"

    class Meta:
        db_table = 'notification'
