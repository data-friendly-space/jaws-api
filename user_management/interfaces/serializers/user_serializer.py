from rest_framework import serializers

from user_management.models import User


class UserTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    country = serializers.CharField(max_length=255)
    profile_image = serializers.URLField(allow_null=True, required=False)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to transform User model to UserTO format.
    """

    class Meta:
        model = User
        fields = ["id", "name", "lastname", "email", "country", "profile_image"]
