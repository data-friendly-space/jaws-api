from tokenize import TokenError

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions.exceptions import UnauthorizedException, BadRequestException, InternalServerErrorException
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from user_management.interfaces.serializers.token_serializer import UserTokenSerializer
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.repository.user_repository_impl import UserRepositoryImpl
from user_management.service.users_service import UsersService
from user_management.usecases.get_user_by_email_uc import GetUserByEmailUC
from user_management.usecases.get_users_uc import GetUsersUC
from user_management.usecases.sign_in_uc import SignInUC
from user_management.usecases.sign_up_uc import SignUpUC


class UsersServiceImpl(UsersService):

    def __init__(self):
        self.get_users_uc = GetUsersUC.get_instance()
        self.sign_in_uc = SignInUC.get_instance()
        self.sign_up_uc = SignUpUC.get_instance()
        self.get_user_by_email_uc = GetUserByEmailUC.get_instance()

    def get_users(self, query_options: QueryOptions):
        return api_response_success("Users retrieved successfully",
                                    UserSerializer(self.get_users_uc.exec(UserRepositoryImpl(), query_options),
                                                   many=True).data,
                                    status.HTTP_200_OK)

    def sign_up(self, name, lastname, email, password):
        if not email or not password or not email:
            raise BadRequestException("All fields are mandatory", None)
        if self.get_user_by_email_uc.exec(UserRepositoryImpl(), email):
            raise BadRequestException("User already exists", None)
        self.sign_up_uc.exec(UserRepositoryImpl(), name, lastname, email, password)
        return api_response_success("User successfully created", None, status.HTTP_201_CREATED)

    def sign_in(self, email, password):
        userTO = self.get_user_by_email_uc.exec(UserRepositoryImpl(), email)
        if not userTO or not check_password(password, userTO.password):
            raise BadRequestException("Incorrect email or password")
        try:
            return api_response_success("User authenticated", UserTokenSerializer(userTO).data, status.HTTP_200_OK)
        except ValueError as e:
            raise UnauthorizedException(str(e), None)

    def refresh_token(self, refresh_token):
        if not refresh_token:
            raise BadRequestException(
                "Refresh token is required.", None)

        try:
            # Attempt to decode the refresh token and generate a new access token
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return api_response_success(
                "Access granted", {"jwt_access_token": new_access_token},
                status.HTTP_200_OK
            )
        except TokenError as e:
            # Handle cases where the refresh token is invalid or expired
            raise UnauthorizedException(
                "Invalid or expired refresh token.", None
            )

    def verify_token(self, auth_header):

        if not auth_header or not auth_header.startswith('Bearer '):
            # Return false if the token is missing or improperly formatted
            raise UnauthorizedException("Unauthorized", {'is_authenticated': False})

        # Extract the token part from the header
        token = auth_header.split(' ')[1]

        # Instantiate JWTAuthentication to validate the token
        jwt_auth = JWTAuthentication()

        try:
            # Validate the token and get the user (if valid)
            jwt_auth.get_validated_token(token)
            return api_response_success("Is authenticated", {'isAuthenticated': True}, status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            # Token is invalid or expired
            raise UnauthorizedException("Session expired", {'is_authenticated': False})
