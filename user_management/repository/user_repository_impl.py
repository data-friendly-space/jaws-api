from user_management.contract.repository.user_repository import UserRepository
from user_management.models import User


class UserRepositoryImpl(UserRepository):
    def get_all(self):
        """
        Retrieve all users from the database.
        """
        return User.objects.all()

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
