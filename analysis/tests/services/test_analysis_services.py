from django.test import TestCase

from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException


class TestAnalysisService(TestCase):

    databases = {'analysis_db'}

    def setUp(self):
        self.service = AnalysisServiceImpl()
        self.test_sector = Sector.objects.create(
            id="test-sector-1",
            name="Sector test"
        )
        self.test_disaggregation = Disaggregation.objects.create(
            id="test-disaggregation-1",
            name="Disaggregation test"
        )

    def test_validate_scope_fields_invalid_date(self):
        scope = {
            "title": "Test Analysis",
            "objetives": "Test Objectives",
            "start_date": "2024-12-31",
            "end_date": "2024-01-01",
        }

        with self.assertRaises(BadRequestException) as context:
            self.service.validate_scope_fields(scope, [self.test_sector])
        self.assertEqual(str(context.exception), 'Start date must be before end date')

    def test_validate_scope_fields_no_data(self):
        scope = {}
        with self.assertRaises(BadRequestException) as context:
            self.service.validate_scope_fields(scope, [])
        self.assertEqual(str(context.exception), 'Missing field')

    def test_get_sectors_with_valid_sectors(self):
        sectors = self.service.get_sectors(["test-sector-1"])
        self.assertEqual(self.test_sector, sectors.first())

    def test_get_disaggregations_with_valid_disaggregations(self):
        disaggregations = self.service.get_disaggregations(["test-disaggregation-1"])
        self.assertEqual(self.test_disaggregation, disaggregations.first())
