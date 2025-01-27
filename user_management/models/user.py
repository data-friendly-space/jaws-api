"""This module contains the user model"""
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """Handles the user management"""

    def create_user(self, email, password=None, **extra_fields):
        """Normalize and validate data before creating a user"""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """User model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    profile_image = models.URLField(blank=True, null=True)
    position = models.ForeignKey('user_management.Position', on_delete=models.SET_NULL, null=True)
    affiliation = models.ForeignKey('user_management.Affiliation', on_delete=models.SET_NULL, null=True)
    ui_configuration = models.OneToOneField('user_management.UiConfiguration', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    def __str__(self):
        return f"{self.name} {self.lastname}"

    class Meta:
        db_table = 'user'

    @classmethod
    def from_to(cls, user_to):
        """
        Creates a User instance from a UserTO instance without saving it.

        Args:
            user_to (UserTO): Transfer Object containing the User data.

        Returns:
            User: An instance of the User model.
        """
        from user_management.contract.to.user_to import UserTO
        from user_management.models.position import Position
        from user_management.models.affiliation import Affiliation
        from user_management.models.ui_configuration import UiConfiguration
        if user_to is None:
            return None

        if not isinstance(user_to, UserTO):
            raise ValueError("The argument must be an instance of UserTO")

        # Resolve ForeignKey and OneToOneField relationships
        position_instance = Position.from_to(user_to.position) if user_to.position else None
        affiliation_instance = Affiliation.from_to(user_to.affiliation) if user_to.affiliation else None
        ui_configuration_instance = (
            UiConfiguration.from_to(user_to.uiConfiguration) if user_to.uiConfiguration else None
        )

        # Create the User instance without saving
        user_instance = cls(
            id=uuid.UUID(user_to.id) if user_to.id else None,
            name=user_to.name,
            lastname=user_to.lastname,
            email=user_to.email,
            country=user_to.country,
            profile_image=user_to.profileImage,
            position=position_instance,
            affiliation=affiliation_instance,
            ui_configuration=ui_configuration_instance,
            is_active=True,  # Default value; adjust if provided in UserTO
        )

        return user_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
