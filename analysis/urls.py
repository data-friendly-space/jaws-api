"""This module contains the urls related with analysis stuff"""

from django.urls import path

from analysis.command.load_administrative_divisions import load_administrative_divisions
from analysis.interfaces.controllers.create_analysis_controller import (
    create_analysis_controller,
)
from analysis.interfaces.controllers.get_administrative_division_controller import (
    get_administrative_division_controller,
)
from analysis.interfaces.controllers.get_analysis_by_id_controller import (
    get_analysis_by_id_controller,
)
from analysis.interfaces.controllers.get_analysis_controller import (
    get_analysis_controller,
)
from analysis.interfaces.controllers.put_analysis_scope_controller import (
    put_analysis_scope_controller,
)

urlpatterns = [
    path("", get_analysis_controller, name="get_analyses"),
    path("create", create_analysis_controller, name="create_analysis"),
    path(
        "load-administrative-divisions",
        load_administrative_divisions,
        name="load_administrative_divisions",
    ),
    path(
        "administrative-divisions",
        get_administrative_division_controller,
        name="get_administrative_divisions",
    ),
    path("<slug:id>", get_analysis_by_id_controller, name="get_analysis"),
    path("<slug:id>/update", put_analysis_scope_controller, name="put_analysis"),
]
