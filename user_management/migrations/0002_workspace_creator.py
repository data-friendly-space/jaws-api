# Generated by Django 5.0.6 on 2024-12-12 02:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from user_management.models.user import User


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_userorganizationrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='creator',
            field=models.ForeignKey(
                default="4e469429-5be2-4033-bcac-1275cd44ac63",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
