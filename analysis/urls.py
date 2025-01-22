"""This module contains the urls related with analysis stuff"""

from django.urls import path

from analysis.interfaces.controllers.add_location_controller import add_location_controller
from analysis.interfaces.controllers.assign_or_update_analysis_framework_controller import \
    assign_or_update_analysis_framework_controller
from analysis.interfaces.controllers.create_analysis_controller import (
    create_analysis_controller,
)
from analysis.interfaces.controllers.create_issue_controller import create_issue_controller
from analysis.interfaces.controllers.create_or_update_analysis_question_controller import \
    create_or_update_analysis_question_controller

from analysis.interfaces.controllers.get_administrative_division_controller import (
    get_administrative_division_controller,
)
from analysis.interfaces.controllers.get_analysis_by_id_controller import (
    get_analysis_by_id_controller,
)
from analysis.interfaces.controllers.get_analysis_frameworks_controller import get_analysis_frameworks_controller
from analysis.interfaces.controllers.get_disaggregations_controller import get_all_disaggregations_controller
from analysis.interfaces.controllers.get_issues_controller import get_issues_controller
from analysis.interfaces.controllers.get_sectors_controller import get_all_sectors_controller
from analysis.interfaces.controllers.get_steps_controller import get_steps_controller
from analysis.interfaces.controllers.put_analysis_scope_controller import (
    put_analysis_scope_controller,
)
from analysis.interfaces.controllers.remove_location_controller import remove_location_controller
from analysis.interfaces.controllers.update_steps_controller import update_steps_controller
from analysis.interfaces.controllers.upload_analysis_framework_controller import upload_analysis_framework_controller

urlpatterns = [
    path("create", create_analysis_controller, name="create_analysis"),
    path("get-steps", get_steps_controller, name="get_steps"),
    path("issues/create", create_issue_controller, name="create_issue_controller"),
    path("<int:analysis_id>/issues", get_issues_controller, name="get_issues_controller"),
    path("frameworks", get_analysis_frameworks_controller, name="get_analysis_frameworks_controller"),
    path("frameworks/upload", upload_analysis_framework_controller, name="upload_analysis_framework_controller"),

    path("sectors", get_all_sectors_controller, name="get_all_sectors_controller"),
    path("disaggregations", get_all_disaggregations_controller, name="get_all_disaggregations_controller"),
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
    path("<int:analysis_id>/frameworks/<int:analysis_framework_id>", assign_or_update_analysis_framework_controller,
         name="assign_or_update_analysis_framework_controller"),
    path("<int:analysis_id>/questions", create_or_update_analysis_question_controller,
         name="create_or_update_analysis_question_controller"),
    path("<slug:analysis_id>/update-steps", update_steps_controller, name="update_steps"),
]
