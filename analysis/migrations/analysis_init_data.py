import sys
from django.db import migrations, models

from analysis.command.add_administrative_divisions import add_administrative_divisions
from analysis.models import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.analysis_step import AnalysisStep
from analysis.models.disaggregation import Disaggregation
from analysis.models.pillar import Pillar
from analysis.models.sector import Sector
from analysis.models.sub_pillar import SubPillar


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
    frameworks = ["JIAF", "IFRC", "PAF", "Deep Generic", "Test Framework"]

    for framework in frameworks:
        AnalysisFramework.objects.get_or_create(name=framework)

    existing_analyses = Analysis.objects.all()
    mandatory_steps = AnalysisStep.objects.filter(
        models.Q(step_parent__isnull=True, mandatory=True)
        | models.Q(step_parent__mandatory=True, mandatory=True)
    )
    for analysis in existing_analyses:
        analysis.analysis_steps.set(mandatory_steps)


def add_pillars_and_sub_pillars():
    """Add pillars and sub-pillars"""

    # Define the pillars and their respective sub-pillars
    pillars_with_subpillars = {
        "EQ1. Relevance/Appropriateness": [
            "1.1. Alignment with population Needs",
            "1.2 Adaptability to Contextual changes",
            "1.3 General Protection Programming",
            "1.4 Partner Protection Programming",
        ],
        "EQ2 Coherence": [
            "2.2 Complementarity of interventions",
            "3.2 Effectiveness of Programme",
            "3.3 Effectiveness of Implementing",
            "3.4 Effectiveness of Partner Protection",
            "4.3 Efficiency of Management and ",
            "4.4 Optimization of Resources and ",
            "4.5 Limitations and Cost-Effective ",
            "4.6 Cost-Efficiency of Partnership",
            "4.7 Cost-Effectiveness of Resource",
        ],
    }

    framework = AnalysisFramework.objects.get_or_create(name="Test Framework")
    # Create and link SubPillars to their corresponding Pillars
    for pillar_name, sub_pillar_names in pillars_with_subpillars.items():
        pillar = Pillar.objects.create(name=pillar_name)  # Create the Pillar
        framework[0].pillars.add(pillar)
        for sub_pillar_name in sub_pillar_names:
            sub_pillar, _ = SubPillar.objects.get_or_create(name=sub_pillar_name)  # Create or fetch SubPillar
            pillar.sub_pillars.add(sub_pillar)  # Link SubPillar to Pillar



def add_initial_data(apps, schema_editor):
    """Add disaggregations, sectors and administrative divisions"""
    add_disaggregation_data()
    add_sector_data()
    if 'test' not in sys.argv:
        add_administrative_divisions()
    add_frameworks_initial_data()
    add_pillars_and_sub_pillars()


def remove_initial_data(apps, schema_editor):
    """Remove disaggregations, sectors and administrative divisions"""
    Sector.objects.all().delete()
    Disaggregation.objects.all().delete()
    if 'test' not in sys.argv:
        AdministrativeDivision.objects.all().delete()
    AnalysisFramework.objects.all().delete()
    Pillar.objects.all().delete()
    SubPillar.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('analysis', '0001_initial'), ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
