# Generated by Django 5.0.6 on 2024-12-01 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisFramework',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'analysis_framework',
            },
        ),
        migrations.CreateModel(
            name='Disaggregation',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'disaggregation',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'sector',
            },
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField()),
                ('objetives', models.CharField(max_length=400)),
                ('workspace_id', models.CharField(max_length=36)),
                ('creator', models.CharField(max_length=36)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('analysis_framework', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='analysis.analysisframework')),
                ('disaggregations', models.ManyToManyField(blank=True, to='analysis.disaggregation')),
                ('sectors', models.ManyToManyField(to='analysis.sector')),
            ],
            options={
                'db_table': 'analysis',
            },
        ),
    ]
