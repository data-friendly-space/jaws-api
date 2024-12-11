from django.contrib.auth.hashers import make_password

from common.exceptions.exceptions import NotFoundException
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.user_repository import UserRepository
from user_management.contract.to.user_to import UserTO
from user_management.models import User


class UserRepositoryImpl(UserRepository):
    """Contains the database access for user model"""
    def get_user_by_filters(self, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        users_found = User.objects.filter(**filters).first()
        return UserTO.from_model(users_found)

    def sign_up(self, name, lastname, email, password):
        return User.objects.create(
            lastname=lastname,
            name=name,
            email=email,
            password=make_password(password)
        )

    def get_user_by_email(self, email):
        user = User.objects.filter(email=email).first()
        return UserTO.from_model(user)

    def get_all(self, query_options: QueryOptions):
        users_query = User.objects.all()
        exclude_fields = ["password"]
        users = query_options.filter_and_exec_queryset(
            users_query, model=User, exclude_fields=exclude_fields
        )
        return UserTO.fromModels(users)

    def get_by_id(self, obj_id):
        try:
            return User.objects.get(id=obj_id)
        except User.DoesNotExist:
            return None

    def delete_by_id(self, obj_id):
        try:
            user = User.objects.get(id=obj_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def update(self, obj_id, data):
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
