"""User management URL Configuration"""

from django.urls import include, path

from user_management.interfaces.controllers.get_roles_and_permissions_controller import (
    get_roles_and_permissions_controller,
)
from user_management.interfaces.controllers.refresh_token_controller import (
    refresh_token_controller,
)
from user_management.interfaces.controllers.sign_in_controller import sign_in_controller
from user_management.interfaces.controllers.sign_in_with_access_token_controller import (
    sign_in_with_access_token_controller,
)
from user_management.interfaces.controllers.sign_up_controller import sign_up_controller
from user_management.interfaces.controllers.verify_token_controller import (
    verify_token_controller,
)

urlpatterns = [
    path("roles/", get_roles_and_permissions_controller, name="get_roles"),
    path("sign-in", sign_in_controller, name="sign_in"),
    path(
        "sign-in-with-access-token",
        sign_in_with_access_token_controller,
        name="sign_in_with_access_token",
    ),
    path("sign-up", sign_up_controller, name="sign_up"),
    path("token-refresh", refresh_token_controller, name="token_refresh"),
    path("session-verify", verify_token_controller, name="session_verify"),
    path("users/", include("user_management.urls.user-urls")),
    path("workspaces/", include("user_management.workspace-urls")),
    path("organizations/", include("user_management.urls.organization-urls")),
]
