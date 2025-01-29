"""User management URL Configuration"""

from django.urls import path

from analysis.interfaces.controllers.get_analysis_controller import (
    get_analysis_controller,
)
from user_management.interfaces.controllers.create_workspace_controller import (
    create_workspace_controller,
)
from user_management.interfaces.controllers.get_workspace_by_id import (
    get_workspaces_by_id_controller,
)

urlpatterns = [
    path("create", create_workspace_controller, name="create_workspace"),
    path(
        "<str:workspace_id>/analyses",
        get_analysis_controller,
        name="get_analysis_controller",
    ),
    path(
        "<str:workspace_id>",
        get_workspaces_by_id_controller,
        name="workspace_by_id",
    ),
]
