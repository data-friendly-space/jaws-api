from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class UserTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    tokens = TokenSerializer(read_only=True)

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)

        return {
            "user_id": instance.id,
            "email": instance.email,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }
