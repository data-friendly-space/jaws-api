"""Contains the data role model"""
from django.db import models

from common.models.base_model import BaseModel


class DataRole(BaseModel,models.Model):
    """Dataset Data Role model"""
    name = models.CharField(max_length=255)

    class Meta:
        """Table's metadata"""
        db_table = "data_roles"

    @classmethod
    def from_to(cls, data_role_to):
        """
        Creates a DataRole instance from a DataRoleTO instance without saving it.

        Args:
            data_role_to (DataRoleTO): Transfer Object containing the DataRole data.

        Returns:
            DataRole: An instance of the DataRole model.
        """
        from file_management.contract.dto.data_role_to import DataRoleTO

        if data_role_to is None:
            return None

        if not isinstance(data_role_to, DataRoleTO):
            raise ValueError("The argument must be an instance of DataRoleTO")

        # Create the DataRole instance without saving
        data_role_instance = cls(
            id=data_role_to.id,  # Include only if IDs are passed in the TO
            name=data_role_to.name,
        )

        return data_role_instance
