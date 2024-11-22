from tokenize import TokenError

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from user_management.interfaces.controllers.helpers.api_response import api_response
from user_management.interfaces.serializers.token_serializer import UserTokenSerializer
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.models import User
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

    def get_users(self):
        return UserSerializer(self.get_users_uc.exec(UserRepositoryImpl()), many=True).data

    def sign_up(self, name, lastname, email, password):

        if not email or not password or not email:
            return api_response("All fields are mandatory", None, status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return api_response("User already exists", None, status.HTTP_400_BAD_REQUEST)
        self.sign_up_uc.exec(UserRepositoryImpl(), name, lastname, email, password)
        return api_response("User successfully created", status.HTTP_201_CREATED)

    def sign_in(self, email, password):
        userTO = self.get_user_by_email_uc.exec(UserRepositoryImpl(), email)
        if not userTO or not check_password(password, userTO.password):
            raise ValueError("Incorrect email or password")
        try:
            return api_response("User authenticated", UserTokenSerializer(userTO).data, status.HTTP_200_OK)
        except ValueError as e:
            return api_response(str(e), None, status.HTTP_401_UNAUTHORIZED)

    def refresh_token(self, refresh_token):
        if not refresh_token:
            return api_response(
                "Refresh token is required.", None,
                status.HTTP_400_BAD_REQUEST
            )

        try:
            # Attempt to decode the refresh token and generate a new access token
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return api_response(
                "Access granted", {"jwt_access_token": new_access_token},
                status.HTTP_200_OK
            )
        except TokenError as e:
            # Handle cases where the refresh token is invalid or expired
            return api_response(
                "Invalid or expired refresh token.", None,
                status.HTTP_401_UNAUTHORIZED
            )

    def verify_token(self, auth_header):

        if not auth_header or not auth_header.startswith('Bearer '):
            # Return false if the token is missing or improperly formatted
            return api_response("Unauthorized", {'is_authenticated': False}, status.HTTP_401_UNAUTHORIZED)

        # Extract the token part from the header
        token = auth_header.split(' ')[1]

        # Instantiate JWTAuthentication to validate the token
        jwt_auth = JWTAuthentication()

        try:
            # Validate the token and get the user (if valid)
            jwt_auth.get_validated_token(token)
            return api_response("Is authenticated", {'is_authenticated': True}, status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            # Token is invalid or expired
            return api_response("Session expired", {'is_authenticated': False}, status.HTTP_401_UNAUTHORIZED)
