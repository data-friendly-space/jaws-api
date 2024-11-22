from typing import Optional

from user_management.contract.to.affiliattion_to import AffiliationTO
from user_management.contract.to.organization_to import OrganizationTO
from user_management.contract.to.position_to import PositionTO
from user_management.contract.to.ui_configuration_to import UiConfigurationTO
from user_management.models import User


class UserTO:
    def __init__(
            self,
            id: int,
            name: str,
            password: str,
            lastname: str,
            email: str,
            country: str,
            position: Optional[dict],
            affiliation: Optional[dict],
            organization: Optional[dict],
            uiConfiguration: Optional[dict],
            profileImage: Optional[str] = None
    ):
        self.id = id
        self.password = password
        self.name = name
        self.lastname = lastname
        self.email = email
        self.country = country
        self.position = position
        self.affiliation = affiliation
        self.organization = organization
        self.uiConfiguration = uiConfiguration
        self.profileImage = profileImage

    @classmethod
    def from_model(cls, instance: User):
        if instance is None:  # Handle case when instance is None
            return None
        """Transforms User instance into a UserTO representation."""
        return cls(
            id=instance.id,
            name=instance.name,
            password=instance.password,
            lastname=instance.lastname,
            email=instance.email,
            country=instance.country,
            position=PositionTO.from_model(instance.position),
            affiliation=AffiliationTO.from_model(instance.affiliation),
            organization=OrganizationTO.from_model(instance.organization),
            uiConfiguration=UiConfigurationTO.from_model(instance.ui_configuration),
            profileImage=instance.profile_image,
        )

    @classmethod
    def fromModels(self, users):
        """
        Transform a list of User model instances into a list of UserTO instances.
        """
        return [self.from_model(user) for user in users]
