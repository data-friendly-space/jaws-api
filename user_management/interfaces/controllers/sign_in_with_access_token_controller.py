"""Contains the controller for signing in an user without a password"""
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from user_management.service.impl.users_service_impl import UsersServiceImpl

@api_view(["POST"])
def sign_in_with_access_token_controller(request):
    """Sign in an user with an access token"""
    token = request.query_params.get("access_token")

    user_service = UsersServiceImpl()
    return api_response_success(
        data=user_service.sign_in_with_access_token(token)
    )