"""This module contains the issue model"""
from django.db import models
from django.db.models import ForeignKey, ManyToManyField

import charts
from analysis.contract.to.issue_to import IssueTO
from analysis.models.disaggregation import Disaggregation
from analysis.models.entry import Entry
from charts.models import Chart


class Issue(models.Model):
    """Issue model"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    information_gaps = models.CharField(max_length=600)
    assumptions = models.CharField(max_length=600)
    disaggregation = ForeignKey(Disaggregation, on_delete=models.CASCADE)
    entries = ManyToManyField(Entry, blank=True)
    charts = models.ManyToManyField(Chart, blank=True)

    class Meta:
        """Table's metadata"""
        db_table = 'issue'

    @classmethod
    def from_to(cls, issue_to):
        """
        Creates an Issue instance from an IssueTO instance without saving it.

        Args:
            issue_to (IssueTO): Transfer Object containing the Issue data.

        Returns:
            Issue: An instance of the Issue model.
        """
        if issue_to is None:
            return None

        if not isinstance(issue_to, IssueTO):
            raise ValueError("The argument must be an instance of IssueTO")

        # Create the Issue instance without saving
        issue_instance = cls(
            id=issue_to.id,  # Include only if IDs are passed in the TO
            name=issue_to.name,
            description=issue_to.description,
            information_gaps=issue_to.informationGaps,
            assumptions=issue_to.assumptions,
            entries= Entry.from_tos(issue_to.entries),
            charts=Entry.from_tos(issue_to.charts),
            disaggregation=Disaggregation.from_to(issue_to.disaggregation)
        )

        return issue_instance
