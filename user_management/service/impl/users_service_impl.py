"""Contains the users service"""
from tokenize import TokenError

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.repository.impl.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.use_cases.get_analyses_uc import GetAnalysesUC
from common.exceptions.exceptions import (
    NotFoundException,
    UnauthorizedException,
    BadRequestException,
)
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from common.use_case.get_all_uc import GetAllUC as GetUsersUC
from interaction_notification_mngr.repository.notification_repository_impl import (
    NotificationRepositoryImpl,
)
from interaction_notification_mngr.service.utils.messages import (
    ORGANIZATION_INVITE_MESSAGE,
    ANALYSIS_INVITE_MESSAGE,
)
from interaction_notification_mngr.usecases.send_notification_to_user_uc import (
    SendNotificationToUserUC,
)
from user_management.contract.io.invite_user_analysis_in import InviteUserAnalysisIn
from user_management.contract.io.invite_user_in import InviteUserIn
from user_management.contract.io.sign_in_in import SignInIn
from user_management.contract.io.sign_up_in import SignUpIn
from user_management.interfaces.serializers.token_serializer import UserTokenSerializer
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.repository.impl.organization_repository_impl import (
    OrganizationRepositoryImpl,
)
from user_management.repository.impl.user_repository_impl import UserRepositoryImpl
from user_management.repository.impl.workspace_repository_impl import WorkspaceRepositoryImpl
from user_management.service.users_service import UsersService
from user_management.usecases.add_user_to_workspace_uc import AddUserToWorkspaceUC
from user_management.usecases.get_user_uc_by_filters_uc import GetUserByFiltersUC
from user_management.usecases.invite_user_to_analysis_uc import InviteUserToAnalysisUC
from user_management.usecases.invite_user_to_organization_uc import (
    InviteUserToOrganizationUC,
)
from user_management.usecases.is_user_in_analysis_uc import IsUserInAnalysisUC
from user_management.usecases.sign_in_uc import SignInUC
from user_management.usecases.sign_up_uc import SignUpUC


class UsersServiceImpl(UsersService):
    """Business logic for user management"""
    def __init__(self):
        self.get_users_uc = GetUsersUC.get_instance()
        self.sign_in_uc = SignInUC.get_instance()
        self.sign_up_uc = SignUpUC.get_instance()
        self.get_user_by_filters = GetUserByFiltersUC.get_instance()
        self.get_analysis_uc = GetAnalysesUC.get_instance()
        self.notify_user_uc = SendNotificationToUserUC.get_instance()
        self.invite_user_to_org_uc = InviteUserToOrganizationUC.get_instance()
        self.invite_user_to_analysis_uc = InviteUserToAnalysisUC.get_instance()
        self.add_user_to_workspace_uc = AddUserToWorkspaceUC.get_instance()
        self.sign_in_uc = SignInUC.get_instance()
        self.is_user_in_analysis_uc = IsUserInAnalysisUC.get_instance()
        self.repository = UserRepositoryImpl()

    def invite_user_to_org(self, invite_user_in: InviteUserIn):
        """Business logic to invite user to an organization"""
        if not invite_user_in.is_valid():
            raise BadRequestException("Invitation not valid", invite_user_in.errors)
        data = invite_user_in.validated_data
        user = self.get_user_by_filters.exec(self.repository, email=data["email"])
        if user is None:
            raise NotFoundException("User not found")
        user_org_role = self.invite_user_to_org_uc.exec(
            OrganizationRepositoryImpl(), user.id, data["id"], data["role_id"]
        )
        self.notify_user_uc.exec(
            NotificationRepositoryImpl(),
            {
                "user_id": user.id,
                "message": ORGANIZATION_INVITE_MESSAGE
                + " "
                + user_org_role.organization.name,
            },
        )

    def invite_user_to_analysis(self, invite_user_in: InviteUserAnalysisIn):
        """Business logic to invite user to an analysis"""
        if not invite_user_in.is_valid():
            raise BadRequestException("Invitation not valid", invite_user_in.errors)
        data = invite_user_in.validated_data
        user = self.get_user_by_filters.exec(self.repository, email=data["email"])
        if user is None:
            raise NotFoundException("User not found")
        analysis = self.get_analysis_uc.exec(
            AnalysisRepositoryImpl(), None, id=data["id"]
        )
        if analysis is None or len(analysis) != 1:
            raise NotFoundException("Analysis not found")
        self.invite_user_to_analysis_uc.exec(
            AnalysisRepositoryImpl(), user.id, data["id"], data["role_id"]
        )
        self.add_user_to_workspace_uc.exec(
            WorkspaceRepositoryImpl(), user.id, analysis[0].workspaceId, None
        )
        self.notify_user_uc.exec(
            NotificationRepositoryImpl(),
            {
                "user_id": user.id,
                "message": ANALYSIS_INVITE_MESSAGE + " " + analysis[0].title,
            },
        )

    def get_users(self, query_options: QueryOptions):
        """Business logic to retrieve all users"""
        users = self.get_users_uc.exec(self.repository, query_options)
        if not users:
            raise NotFoundException("Users not found")
        return UserSerializer(users, many=True).data

    def sign_up(self, sign_up_in: SignUpIn):
        """Business logic to sign up user"""
        if not sign_up_in.is_valid():
            raise BadRequestException("All fields are mandatory", sign_up_in.errors)
        data = sign_up_in.validated_data
        if (
            self.get_user_by_filters.exec(self.repository, email=data["email"])
            is not None
        ):
            raise BadRequestException("User already exists", None)
        self.sign_up_uc.exec(self.repository, **data)

    def sign_in(self, sign_in_in: SignInIn):
        """Business logic to sign in"""
        if not sign_in_in.is_valid():
            raise BadRequestException("All fields are mandatory", sign_in_in.errors)
        data = sign_in_in.validated_data
        user_to = self.get_user_by_filters.exec(
            self.repository, email=data["email"]
        )
        if not user_to or not check_password(data["password"], user_to.password):
            raise BadRequestException("Incorrect email or password")
        try:
            return UserTokenSerializer(user_to).data
        except ValueError as e:
            raise UnauthorizedException(str(e), None) from e

    def sign_in_with_access_token(self, token: str):
        """Sign in a user with an access token"""
        if not token:
            raise UnauthorizedException(
                "The token is required", {"is_authenticated": False}
            )

        jwt_auth = JWTAuthentication()
        try:
            token_decoded = jwt_auth.get_validated_token(token)
            user_to = self.get_user_by_filters.exec(
                self.repository, id=token_decoded.payload["user_id"]
            )
            if not user_to:
                raise BadRequestException("User not found")
            return UserTokenSerializer(user_to).data
        except (ValueError, InvalidToken) as e:
            raise UnauthorizedException(str(e), None) from e

    def refresh_token(self, refresh_token):
        """Business logic to process refresh token"""
        if not refresh_token:
            raise BadRequestException("Refresh token is required.", None)
        try:
            # Attempt to decode the refresh token and generate a new access token
            token = RefreshToken(refresh_token)
            return str(token.access_token)
        except TokenError as e:
            # Handle cases where the refresh token is invalid or expired
            raise UnauthorizedException("Invalid or expired refresh token.", None) from e

    def verify_token(self, auth_header):
        """Business logic to verify token"""
        if not auth_header or not auth_header.startswith("Bearer "):
            # Return false if the token is missing or improperly formatted
            raise UnauthorizedException("Unauthorized", {"is_authenticated": False})

        # Extract the token part from the header
        token = auth_header.split(" ")[1]

        # Instantiate JWTAuthentication to validate the token
        jwt_auth = JWTAuthentication()

        try:
            jwt_auth.get_validated_token(token)
            return api_response_success(
                "Is authenticated", {"isAuthenticated": True}, status.HTTP_200_OK
            )
        except (InvalidToken, TokenError) as e:
            raise UnauthorizedException("Session expired", {"is_authenticated": False}) from e

    def is_user_in_analysis(self, user_id: str, analysis_id: int) -> bool:
        """Verify if the user is in the analysis"""
        return self.is_user_in_analysis_uc.exec(self.repository, user_id, analysis_id)
