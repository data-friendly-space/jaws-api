"""This module contains the issue model"""
from django.db import models, transaction
from django.db.models import ForeignKey, ManyToManyField

from common.models.base_model import BaseModel


class Issue(models.Model, BaseModel):
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
        Creates or updates an Issue instance from an IssueTO instance.

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

        # Build the defaults dictionary
        defaults = {
            "name": issue_to.name,
            "description": issue_to.description,
            "information_gaps": issue_to.informationGaps,
            "assumptions": issue_to.assumptions,
            "disaggregation": Disaggregation.from_to(issue_to.disaggregation) if issue_to.disaggregation else None,
            "analysis_id": issue_to.analysisId
        }

        # Remove keys with None values to avoid overwriting
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # Update or create the Issue instance
            issue_instance, created = cls.objects.update_or_create(
                id=issue_to.id,
                defaults=defaults,
            )

            # Handle ManyToMany relationships only if the instance is created or if fields are provided
            if created or issue_to.entries is not None:
                entries = Entry.from_tos(issue_to.entries) if issue_to.entries else []
                issue_instance.entries.set(entries)

            if created or issue_to.charts is not None:
                charts = Chart.from_tos(issue_to.charts) if issue_to.charts else []
                issue_instance.charts.set(charts)

        return issue_instance
