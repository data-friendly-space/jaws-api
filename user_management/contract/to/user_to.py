'''This module contains the User Transfer Object'''
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from common.contract.to.base_to import BaseTO
from user_management.contract.to.affiliattion_to import AffiliationTO
from user_management.contract.to.organization_to import OrganizationTO
from user_management.contract.to.position_to import PositionTO
from user_management.contract.to.ui_configuration_to import UiConfigurationTO
from user_management.models import User


@dataclass
class UserTO(BaseTO):
    id: str
    name: str
    password: str
    lastname: str
    email: str
    country: str
    position: Optional[dict]
    affiliation: Optional[dict]
    organization: Optional[dict]
    uiConfiguration: Optional[dict]
    profileImage: Optional[str] = None

    @classmethod
    def from_model(cls, instance: User) -> 'UserTO | None':
        """Transforms User instance into a UserTO representation."""
        if instance is None:  # Handle case when instance is None
            return None
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

    def to_dict(self) -> Dict:
        return asdict(self)
