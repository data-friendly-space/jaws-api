"""Interaction and nofitication manager URL Configuration"""
from django.urls import path

from interac_not_manager.interfaces.get_user_notifications_controller import get_user_notifications_controller

urlpatterns = [
    path('notifications/user', get_user_notifications_controller,
         name='get_user_notifications_controller'),

]
