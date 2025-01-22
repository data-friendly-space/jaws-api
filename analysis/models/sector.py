"""This module contains the sector model"""
from django.db import models

from analysis.contract.to.issue_to import IssueTO


class Sector(models.Model):
    """Sector model"""
    name = models.CharField(max_length=100)

    class Meta:
        """Table's metadata"""
        db_table = 'sector'

    @classmethod
    def from_to(cls, issue_to):
        """
        Creates an issue model from an issue TO
        """
        if not isinstance(issue_to, IssueTO):
            raise ValueError("The argument must be an IssueTO")

        return cls(
            id=issue_to.id,
            name=issue_to.name
        )
