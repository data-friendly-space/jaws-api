from django.urls import path

from analysis.interfaces.controllers import get_analysis_controller
from analysis.interfaces.controllers import analysis_scope_controller

urlpatterns = [
    path(":id", get_analysis_controller, name="get_analysis"),
    path(":id/scope", analysis_scope_controller, name="put_analysis_scope")
]
