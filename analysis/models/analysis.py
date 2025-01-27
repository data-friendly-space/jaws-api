"""This module contains the analysis model"""
from django.db import models, transaction


class Analysis(models.Model):
    """Analysis model"""

    class Meta:
        """Table metadata"""
        db_table = 'analysis'

    workspace = models.ForeignKey(
        "user_management.Workspace",
        on_delete=models.CASCADE,
        related_name="analyses"
    )
    title = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField()
    disaggregations = models.ManyToManyField('analysis.Disaggregation', blank=True)
    sectors = models.ManyToManyField('analysis.Sector')
    objectives = models.CharField(max_length=400)
    creator = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)
    locations = models.ManyToManyField('analysis.AdministrativeDivision')
    analysis_steps = models.ManyToManyField('analysis.AnalysisStep')
    datasets = models.ManyToManyField(
        'file_management.Dataset', related_name='analyses',
        through="analysis.AnalysisDataset")
    analysis_framework = models.ForeignKey('analysis.AnalysisFramework', on_delete=models.CASCADE, null=True,
                                           blank=True, related_name="analysis_framework")

    def save(self, *args, **kwargs):
        from analysis.models.analysis_step import AnalysisStep

        is_new = self.pk is None

        if is_new:
            with transaction.atomic():
                super().save(*args, **kwargs)
                mandatory_steps = AnalysisStep.objects.filter(
                    models.Q(step_parent__isnull=True, mandatory=True) |
                    models.Q(step_parent__mandatory=True, mandatory=True))
                self.analysis_steps.set(mandatory_steps)


    def get_all_locations_with_hierarchy(self):
        """Get all related locations with their hierarchies"""
        locations_with_hierarchy = {}
        for location in self.locations.all():
            locations_with_hierarchy[location.id] = location.get_hierarchy()
        return locations_with_hierarchy

    @classmethod
    def from_to(cls, analysis_to):
        """
        Creates an Analysis instance from an AnalysisTO instance without saving it.

        Args:
            analysis_to (AnalysisTO): Transfer Object containing the Analysis data.

        Returns:
            Analysis: An instance of the Analysis model.
        """
        from analysis.models.disaggregation import Disaggregation
        from analysis.contract.to.analysis_to import AnalysisTO
        from common.test_utils import User
        from analysis.models.analysis_framework import AnalysisFramework

        if analysis_to is None:
            return None

        if not isinstance(analysis_to, AnalysisTO):
            raise ValueError("The argument must be an instance of AnalysisTO")

        # Resolve ForeignKey relationships

        # Create the Analysis instance without saving
        analysis_instance = cls(
            title=analysis_to.title,
            objectives=analysis_to.objectives,
            creator=User.from_to(analysis_to.creator),
            analysis_framework=AnalysisFramework.from_to(analysis_to.analysisFramework),
            start_date=analysis_to.startDate,
            end_date=analysis_to.endDate,
            workspace_id=analysis_to.workspace['id'],
            disaggregations=Disaggregation.from_to(analysis_to.disaggregations),
        )

        return analysis_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]

    def set_many_to_many_relations(self, analysis_to):
        """
        Sets the ManyToMany relationships for the Analysis instance.

        Args:
            analysis_to (AnalysisTO): Transfer Object containing the Analysis data.
        """
        from analysis.models.disaggregation import Disaggregation
        from analysis.models.sector import Sector
        from analysis.models.analysis_step import AnalysisStep
        from analysis.models.administrative_division import AdministrativeDivision
        # Resolve ManyToMany relationships
        disaggregations_instances = [Disaggregation.from_to(d) for d in
                                     analysis_to.disaggregations] if analysis_to.disaggregations else []
        sectors_instances = [Sector.from_to(s) for s in analysis_to.sectors] if analysis_to.sectors else []
        locations_instances = [AdministrativeDivision.from_to(l) for l in
                               analysis_to.locations] if analysis_to.locations else []
        analysis_steps_instances = [AnalysisStep.from_to(a) for a in
                                    analysis_to.analysisSteps] if analysis_to.analysisSteps else []

        # Set the relationships
        self.disaggregations.set(disaggregations_instances, clear=True)
        self.sectors.set(sectors_instances, clear=True)
        self.locations.set(locations_instances, clear=True)
        self.analysis_steps.set(analysis_steps_instances, clear=True)


class AnalysisDataset(models.Model):
    """Many to many table for datasets within an analysis"""

    analysis = models.ForeignKey('analysis.Analysis', on_delete=models.CASCADE)
    dataset = models.ForeignKey('file_management.Dataset', on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table = 'analysis_datasets'
