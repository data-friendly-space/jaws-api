'''AdministrativeDivision model module'''
from django.db import models


class AdministrativeDivision(models.Model):
    '''AdministrativeDivision model'''
    ADMIN_LEVEL_CHOICES = [
        (1, 'Country'),
        (2, 'Province/State'),
        (3, 'District'),
        (4, 'City')
    ]

    p_code = models.CharField(
        primary_key=True,
        max_length=10,
        blank=False,
        null=False,
        verbose_name="P-Code")
    location_code = models.CharField(max_length=50, verbose_name="Country Code")
    admin_level = models.PositiveSmallIntegerField(
        choices=ADMIN_LEVEL_CHOICES,
        verbose_name="Admin Level")
    name = models.CharField(max_length=255, verbose_name="Name")
    parent_p_code = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subdivisions",
        verbose_name="Parent P-Code"
    )
    valid_from_date = models.DateField(verbose_name="Valid From Date")

    class Meta:
        '''Table metadata'''
        db_table = "adminisitrative_division"
        verbose_name = "Administrative Division"
        verbose_name_plural = "Administrative Divisions"
        ordering = ['location_code', 'admin_level', 'p_code']

    def __str__(self):
        '''Return the Administrative Division as string'''
        return f"{self.name} ({self.p_code})"
