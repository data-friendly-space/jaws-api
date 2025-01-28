"""This module contains the sector model"""
from django.db import models, transaction

from common.models import BaseModel


class Sector(models.Model, BaseModel):
    """Sector model"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table's metadata"""
        db_table = 'sector'

    @classmethod
    def from_to(cls, sector_to):
        """
        Creates an issue model from an issue TO
        """
        from analysis.contract.to.issue_to import IssueTO

        if not isinstance(sector_to, IssueTO):
            raise ValueError("The argument must be an IssueTO")

        with transaction.atomic():
            # Create the Position instance without saving
            sector_instance = cls(
                id=sector_to.id if sector_to.id else None,
                name=sector_to.name,
            )

        return sector_instance
