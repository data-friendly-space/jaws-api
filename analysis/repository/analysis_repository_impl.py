from analysis.contract.repository.analysis_repository import AnalysisRepository
from analysis.models.analysis import Analysis
from user_management.interfaces.serializers.user_serializer import UserSerializer
from user_management.models import User


class AnalysisRepositoryImpl(AnalysisRepository):
    def get_all(self):
        """
        Retrieve all users from the database.
        """
        users = Analysis.objects.all()
        if not users or len(users) == 0:
            return []
        return UserSerializer(users, many=True).data

    def get_by_id(self, obj_id):
        """
        Retrieve a single user by ID.
        """
        try:
            return Analysis.objects.get(id=obj_id)
        except Analysis.DoesNotExist:
            return None

    def delete_by_id(self, obj_id):
        """
        Delete a user by ID.
        """
        try:
            user = Analysis.objects.get(id=obj_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def update(self, obj_id, data):
        """
        Update a user by ID.
        """
        try:
            user = Analysis.objects.get(id=obj_id)
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
        user = Analysis.objects.create(**data)
        return user
