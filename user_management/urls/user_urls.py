"""User management URL Configuration"""

from django.urls import path

from user_management.interfaces.controllers.get_user_logged_organizations_controller import (
    get_available_user_organizations,
)
from user_management.interfaces.controllers.get_user_logged_workspaces_controller import (
    get_user_logged_workspaces_controller,
)
from user_management.interfaces.controllers.get_users_controller import (
    get_users_controller,
)
from user_management.interfaces.controllers.invite_user_to_analysis_controller import (
    invite_user_to_analysis_controller,
)
from user_management.interfaces.controllers.invite_user_to_organization_controller import (
    invite_user_to_organization_controller,
)

urlpatterns = [
    path("", get_users_controller, name="get_users"),
    path(
        "user/workspaces",
        get_user_logged_workspaces_controller,
        name="get_user_logged_workspaces_controller",
    ),
    path(
        "user/organizations",
        get_available_user_organizations,
        name="get_available_organizations_by_user_id",
    ),
    path(
        "user/invite/organization",
        invite_user_to_organization_controller,
        name="invite_user_to_organization",
    ),
    path(
        "user/invite/analysis",
        invite_user_to_analysis_controller,
        name="invite_user_to_analysis",
    )
]
