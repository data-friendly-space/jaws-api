from django.contrib.auth.hashers import make_password

from common.exceptions.exceptions import NotFoundException
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.user_repository import UserRepository
from user_management.contract.to.user_to import UserTO
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
        user = User.objects.filter(email=email).first()
        return UserTO.from_model(user)

    def get_all(self, query_options: QueryOptions):
        """
        Retrieve all users from the database.
        """
        users_query = User.objects.all()
        if not users_query or not users_query.exists() or len(users_query) == 0:
            raise NotFoundException("No users found")
        users = query_options.filter_and_exec_queryset(users_query)
        return UserTO.fromModels(users)

    def get_by_id(self, obj_id):
        """
        Retrieve a single user by ID.
        """
        return User.objects.get(id=obj_id)

    def delete_by_id(self, obj_id):
        """
        Delete a user by ID.
        """
        user = User.objects.get(id=obj_id)
        return user.delete()

    def update(self, obj_id, data):
        """
        Update a user by ID.
        """
        user = User.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(user, field, value)
        user.save()
        return user

    def create(self, data):
        """
        Add a new user to the database.
        """
        user = User.objects.create(**data)
        return user
