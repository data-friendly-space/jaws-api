"""Interaction and nofitication manager URL Configuration"""
from django.urls import path

from interac_not_manager.interfaces.delete_notification_controller import delete_notification_by_id_controller
from interac_not_manager.interfaces.get_user_notifications_controller import get_user_notifications_controller

urlpatterns = [
    path('notifications/user', get_user_notifications_controller,
         name='get_user_notifications_controller'),
    path('notifications/<int:notification_id>', delete_notification_by_id_controller,
         name='delete_notification_by_id_controller'),

]
