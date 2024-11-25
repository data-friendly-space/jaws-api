from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user_management.contract.to.user_to import UserTO
from user_management.interfaces.serializers.user_serializer import UserSerializer


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class UserTokenSerializer(serializers.Serializer):
    user = UserTO  # Replaced user_id and email with user object
    tokens = TokenSerializer(read_only=True)

    def to_representation(self, instance):
        # Create the refresh token based on the user instance
        refresh = RefreshToken.for_user(instance)

        # Return the structured response with user details and tokens
        return {
            "user": UserSerializer(instance).data,  # Serialize the user using UserTO_
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }
