from abc import ABC

from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.repository.user_repository_impl import UserRepositoryImpl
from user_management.service.users_service import UsersService
from user_management.usecases.get_users_uc import GetUsersUc


class UsersServiceImpl(UsersService, ABC):
    def __init__(self):
        self.get_users_uc = GetUsersUc.get_instance()

    def get_users(self):
        users = self.get_users_uc.exec(UserRepositoryImpl())
        if not users or len(users) == 0:
            return []

        return UserSerializer(users, many=True).data
