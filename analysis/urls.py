"""This module contains the urls related with analysis stuff"""

from django.urls import path

from analysis.interfaces.controllers.add_location_controller import add_location_controller
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
from analysis.interfaces.controllers.remove_location_controller import remove_location_controller

urlpatterns = [
    path("", get_analysis_controller, name="get_analyses"),
    path("create", create_analysis_controller, name="create_analysis"),
    path(
        "administrative-divisions",
        get_administrative_division_controller,
        name="get_administrative_divisions",
    ),
    path(
        "<slug:analysis_id>/add-location/<slug:p_code>",
        add_location_controller,
        name="add_location"
    ),
    path(
        "<slug:analysis_id>/remove-location/<slug:p_code>",
        remove_location_controller,
        name="remove_location"
    ),
    path("<slug:id>", get_analysis_by_id_controller, name="get_analysis"),
    path("<slug:analysis_id>/update", put_analysis_scope_controller, name="put_analysis"),
]
