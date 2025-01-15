"""Urls of the charts app"""
from django.urls import path

from charts.interfaces.controllers.get_charts_controller import get_charts_controller
from charts.interfaces.controllers.save_chart_controller import save_chart_controller


urlpatterns = [
    path(
        "save",
        save_chart_controller,
        name="save"
    ),
    path(
        "get-charts",
        get_charts_controller,
        name="get_charts"
    )
]
