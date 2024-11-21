from django.contrib.auth.hashers import make_password

from user_management.contract.repository.user_repository import UserRepository
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.models import User


class UserRepositoryImpl(UserRepository):
    def sign_up(self, name, lastname, email, password):
        return User.objects.create(
            lastname=lastname,
            name=name,
            email=email,
            password=make_password(password)
        )

    def get_user_by_email(self, email):
        return User.objects.filter(email=email).first()

    def get_all(self):
        """
        Retrieve all users from the database.
        """
        users = User.objects.all()
        if not users or len(users) == 0:
            return []
        return UserSerializer(users, many=True).data

    def get_by_id(self, obj_id):
        """
        Retrieve a single user by ID.
        """
        try:
            return User.objects.get(id=obj_id)
        except User.DoesNotExist:
            return None

    def delete_by_id(self, obj_id):
        """
        Delete a user by ID.
        """
        try:
            user = User.objects.get(id=obj_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def update(self, obj_id, data):
        """
        Update a user by ID.
        """
        try:
            user = User.objects.get(id=obj_id)
            for field, value in data.items():
                setattr(user, field, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None

    def create(self, data):
        """
        Add a new user to the database.
        """
        user = User.objects.create(**data)
        return user
