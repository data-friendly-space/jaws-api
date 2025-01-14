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
    """Insertions"""
    add_pillars_and_sub_pillars()

def remove_initial_data(apps, schema_editor):
    """Remove insertions"""
    Pillar.objects.all().delete()
    SubPillar.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('analysis', '0004_alter_pillar_alias_alter_subpillar_alias'), ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
