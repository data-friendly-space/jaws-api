"""This module contains the issue model"""
from django.db import models
from django.db.models import ForeignKey, ManyToManyField

from common.models.base_model import BaseModel


class Issue(BaseModel):
    """Issue model"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    information_gaps = models.CharField(max_length=600)
    assumptions = models.CharField(max_length=600)
    disaggregation = ForeignKey('analysis.Disaggregation', on_delete=models.CASCADE)
    entries = ManyToManyField('analysis.Entry', blank=True)
    charts = models.ManyToManyField('charts.Chart', blank=True)
    analysis = models.ForeignKey('analysis.Analysis', on_delete=models.CASCADE)

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
        from analysis.models.disaggregation import Disaggregation
        from analysis.models.entry import Entry
        from charts.models import Chart
        from analysis.contract.to.issue_to import IssueTO

        if issue_to is None:
            return None

        if not isinstance(issue_to, IssueTO):
            raise ValueError("The argument must be an instance of IssueTO")

        # Create the Issue instance without ManyToMany fields
        issue_instance = cls(
            id=issue_to.id,  # Include only if IDs are passed in the TO
            name=issue_to.name,
            description=issue_to.description,
            information_gaps=issue_to.informationGaps,
            assumptions=issue_to.assumptions,
            disaggregation=Disaggregation.from_to(issue_to.disaggregation),
            analysis_id=issue_to.analysisId
        )

        # Save the instance to enable ManyToManyField assignments
        issue_instance.save()

        # Assign ManyToMany fields using .set()
        if issue_to.entries:
            issue_instance.entries.set(Entry.from_tos(issue_to.entries))

        if issue_to.charts:
            issue_instance.charts.set(Chart.from_tos(issue_to.charts))

        return issue_instance