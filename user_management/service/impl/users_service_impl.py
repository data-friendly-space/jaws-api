from tokenize import TokenError

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions.exceptions import NotFoundException, UnauthorizedException, BadRequestException
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from common.use_case.get_all_uc import GetAllUC as GetUsersUC
from user_management.contract.io.sign_in_in import SignInIn
from user_management.contract.io.sign_up_in import SignUpIn
from user_management.interfaces.serializers.token_serializer import UserTokenSerializer
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.repository.user_repository_impl import UserRepositoryImpl
from user_management.service.users_service import UsersService
from user_management.usecases.get_user_uc_by_filters_uc import GetUserByFiltersUC
from user_management.usecases.sign_in_uc import SignInUC
from user_management.usecases.sign_up_uc import SignUpUC


class UsersServiceImpl(UsersService):

    def __init__(self):
        self.get_users_uc = GetUsersUC.get_instance()
        self.sign_in_uc = SignInUC.get_instance()
        self.sign_up_uc = SignUpUC.get_instance()
        self.get_user_by_filters = GetUserByFiltersUC.get_instance()

    def get_users(self, query_options: QueryOptions):
        """Business logic to retrieve all users"""
        users = self.get_users_uc.exec(UserRepositoryImpl(), query_options)
        if not users:
            raise NotFoundException("Users not found")
        return UserSerializer(users, many=True).data

    def sign_up(self, sign_up_in: SignUpIn):
        """Business logic to sign up user"""
        if not sign_up_in.is_valid():
            raise BadRequestException("All fields are mandatory", sign_up_in.errors)
        data = sign_up_in.validated_data
        if self.get_user_by_filters.exec(UserRepositoryImpl(), email=data['email']) is not None:
            raise BadRequestException("User already exists", None)
        self.sign_up_uc.exec(UserRepositoryImpl(), **data)

    def sign_in(self, sign_in_in: SignInIn):
        """Business logic to sign in"""
        if not sign_in_in.is_valid():
            raise BadRequestException("All fields are mandatory", sign_in_in.errors)
        data = sign_in_in.validated_data
        user_to = self.get_user_by_filters.exec(UserRepositoryImpl(), email=data['email'])
        if not user_to or not check_password(data['password'], user_to.password):
            raise BadRequestException("Incorrect email or password")
        try:
            return UserTokenSerializer(user_to).data
        except ValueError as e:
            raise UnauthorizedException(str(e), None)

    def refresh_token(self, refresh_token):
        """Business logic to process refresh token"""
        if not refresh_token:
            raise BadRequestException(
                "Refresh token is required.", None)
        try:
            # Attempt to decode the refresh token and generate a new access token
            token = RefreshToken(refresh_token)
            return str(token.access_token)
        except TokenError as e:
            # Handle cases where the refresh token is invalid or expired
            raise UnauthorizedException(
                "Invalid or expired refresh token.", None
            )

    def verify_token(self, auth_header):
        """Business logic to verify token"""
        if not auth_header or not auth_header.startswith('Bearer '):
            # Return false if the token is missing or improperly formatted
            raise UnauthorizedException("Unauthorized", {'is_authenticated': False})

        # Extract the token part from the header
        token = auth_header.split(' ')[1]

        # Instantiate JWTAuthentication to validate the token
        jwt_auth = JWTAuthentication()

        try:
            jwt_auth.get_validated_token(token)
            return api_response_success("Is authenticated", {'isAuthenticated': True}, status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            raise UnauthorizedException("Session expired", {'is_authenticated': False})
