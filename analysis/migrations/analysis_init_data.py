from django.db import migrations, models

from analysis.models.analysis import Analysis
from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.analysis_step import AnalysisStep
from analysis.models.sector import Sector


def analysis_module_init_data(apps, schema_editor):
    sectors = [
        "Inter-sectoral",
        "Camp Coordination and Camp Management",
        "Early Recovery",
        "Education",
        "Emergency Telecommunications",
        "Food Security",
        "Health",
        "Logistics",
        "Nutrition",
        "Protection"
        "Shelter",
        "WASH",
        "Cross cutting issues",
        "Other"
    ]

    frameworks = ["JIAF", "IFRC", "PAF", "Deep Generic"]

    for sector in sectors:
        Sector.objects.get_or_create(name=sector)

    for framework in frameworks:
        AnalysisFramework.objects.get_or_create(name=framework)

    existing_analyses = Analysis.objects.all()
    mandatory_steps = AnalysisStep.objects.filter(
        models.Q(step_parent__isnull=True, mandatory=True)
        | models.Q(step_parent__mandatory=True, mandatory=True)
    )
    for analysis in existing_analyses:
        analysis.analysis_steps.set(mandatory_steps)


def undo_analysis_init_data(apps, schema_editor):
    Sector.objects.all().delete()
    AnalysisFramework.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('analysis', '0007_analysis_framework'), ]

    operations = [
        migrations.RunPython(analysis_module_init_data, undo_analysis_init_data),
    ]
