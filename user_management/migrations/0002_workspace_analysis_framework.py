# Generated by Django 5.1.3 on 2024-12-05 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='analysis_framework',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analysis.analysisframework'),
        ),
    ]
