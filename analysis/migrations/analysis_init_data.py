import sys
from django.db import migrations, models

from analysis.command.add_administrative_divisions import add_administrative_divisions
from analysis.models import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.analysis_step import AnalysisStep
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector


def add_disaggregation_data():
    """Add disaggregation data into the Disaggregation model"""
    disaggregations = [
        {"name": "Geography"},
        {"name": "Sex and age"},
        {"name": "Vulnerable Groups"},
        {"name": "Affected Groups"},
    ]
    for disaggregation in disaggregations:
        Disaggregation.objects.create(**disaggregation)


def add_sector_data():
    """Add sectors data into the Sector model"""
    sectors = [
        {"name": "Inter-sectoral"},
        {"name": "Camp Coordination and Camp Management"},
        {"name": "Early Recovery"},
        {"name": "Education"},
        {"name": "Emergency Telecomunications"},
        {"name": "Food Security"},
        {"name": "Health"},
        {"name": "Logistics"},
        {"name": "Nutritions"},
        {"name": "Protection"},
        {"name": "Shelter"},
        {"name": "WASH"},
        {"name": "Cross Cutting Issues"},
        {"name": "Other"},
    ]
    for sector in sectors:
        Sector.objects.create(**sector)


def add_frameworks_initial_data():
    frameworks = ["JIAF", "IFRC", "PAF", "Deep Generic"]

    for framework in frameworks:
        AnalysisFramework.objects.get_or_create(name=framework)

    existing_analyses = Analysis.objects.all()
    mandatory_steps = AnalysisStep.objects.filter(
        models.Q(step_parent__isnull=True, mandatory=True)
        | models.Q(step_parent__mandatory=True, mandatory=True)
    )
    for analysis in existing_analyses:
        analysis.analysis_steps.set(mandatory_steps)


def add_initial_data(apps, schema_editor):
    """Add disaggregations, sectors and administrative divisions"""
    add_disaggregation_data()
    add_sector_data()
    if 'test' not in sys.argv:
        add_administrative_divisions()
    add_frameworks_initial_data()


def remove_initial_data(apps, schema_editor):
    """Remove disaggregations, sectors and administrative divisions"""
    Sector.objects.all().delete()
    Disaggregation.objects.all().delete()
    if 'test' not in sys.argv:
        AdministrativeDivision.objects.all().delete()
    AnalysisFramework.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('analysis', '0001_initial'), ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
