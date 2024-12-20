"""Contains the tests for analysis service"""

from django.test import TestCase

from analysis.contract.to.administrative_division_dto import AdministrativeDivisionTO
from analysis.interfaces.serializers.administrative_division_serializer import (
    AdministrativeDivisionSerializer,
)
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException, NotFoundException
from common.test_utils import create_logged_in_client
from user_management.models import Organization, Workspace, Role


class TestAnalysisService(TestCase):
    """Class that tests the analysis service"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = AnalysisServiceImpl()
        self.org = Organization.objects.create(name="TestOrganization2")
        self.workspace = Workspace.objects.create(
            title="TestWorksp2ace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.role = Role.objects.get_or_create(role="ADMIN")

        self.test_sector = Sector.objects.create(id=1, name="Sector test")
        self.test_disaggregation = Disaggregation.objects.create(
            id=1, name="Disaggregation test"
        )
        self.test_administrative_division_level_0 = (
            AdministrativeDivision.objects.create(
                p_code="test", name="Test", admin_level=0
            )
        )
        self.test_analysis = Analysis.objects.create(
            id=1,
            title="TestAnalysis1",
            workspace_id=self.workspace.id,
            end_date="2024-12-17",
            creator_id=self.user.id,
        )

    def test_validate_scope_fields_invalid_date(self):
        """Test that an invalid date is not valid"""
        scope = {
            "title": "Test Analysis",
            "objectives": "Test Objectives",
            "start_date": "2024-12-31",
            "end_date": "2024-01-01",
        }

        with self.assertRaises(BadRequestException) as context:
            self.service.validate_scope_fields(scope, [self.test_sector])
        self.assertEqual(str(context.exception), "Start date must be before end date")

    # def test_validate_scope_fields_no_data(self):
    #    """Tests that a scope with no data is invalid"""
    #    scope = {}
    #    with self.assertRaises(BadRequestException) as context:
    #        self.service.validate_scope_fields(scope, [])
    #    self.assertEqual(str(context.exception), "Missing field")

    def test_get_sectors_with_valid_sectors(self):
        """Tests that get sectors with valid sectors works"""
        sectors = self.service.get_sectors([1])
        self.assertEqual(self.test_sector, sectors.first())

    def test_get_disaggregations_with_valid_disaggregations(self):
        """Tests that get disaggregations with valid disaggregations works"""
        disaggregations = self.service.get_disaggregations([1])
        self.assertEqual(self.test_disaggregation, disaggregations.first())

    def test_get_administrative_divisions_with_divisions(self):
        """Tests that getting the administrative divisions works"""
        administrative_divisions = self.service.get_administrative_divisions(
            parent_p_code=None
        )
        administrative_division_to = AdministrativeDivisionTO.from_model(
            self.test_administrative_division_level_0
        )
        self.assertEqual(
            AdministrativeDivisionSerializer(administrative_division_to).data,
            administrative_divisions[0],
        )

    def test_get_administrative_divisions_with_parent_p_code(self):
        """Tests that getting a child administrative division works"""
        administrative_division_level_1 = AdministrativeDivision.objects.create(
            name="test level 1",
            p_code="test-lvl-1",
            parent_p_code=self.test_administrative_division_level_0,
            admin_level=1,
        )
        administrative_division_level_1_to = AdministrativeDivisionTO.from_model(
            administrative_division_level_1
        )
        administrative_divisions = self.service.get_administrative_divisions(
            parent_p_code=self.test_administrative_division_level_0.p_code
        )
        self.assertEqual(
            AdministrativeDivisionSerializer(administrative_division_level_1_to).data,
            administrative_divisions[0],
        )

    def test_get_administrative_divisions_with_no_divisions_fails(self):
        """Tests that getting administritive divisions with no divisions fails"""
        self.test_administrative_division_level_0.delete()
        with self.assertRaises(NotFoundException):
            self.service.get_administrative_divisions(parent_p_code=None)

    def test_add_location_valid(self):
        """
        Tests that adding a location with a correct p_code,
        valid analysis and not existing p_code in the analysis works
        """
        valid_analysis_id = self.test_analysis.id
        valid_p_code = self.test_administrative_division_level_0.p_code
        response = self.service.add_location(valid_analysis_id, valid_p_code)
        self.assertEqual(
            response,
            AdministrativeDivisionSerializer(
                AdministrativeDivisionTO.from_model(
                    self.test_administrative_division_level_0, include_hierarchy=True
                )
            ).data,
        )

    def test_add_location_invalid_p_code(self):
        """Tests that adding a location with a unexisting p_code fails"""
        invalid_p_code = "invalid"
        valid_analysis_id = self.test_analysis.id
        with self.assertRaises(NotFoundException):
            self.service.add_location(valid_analysis_id, invalid_p_code)

    def test_add_location_existing_p_code(self):
        """Tests that adding a location with a existing p_code fails"""
        existing_p_code = self.test_administrative_division_level_0.p_code
        valid_analysis_id = self.test_analysis.id
        self.test_analysis.locations.add(self.test_administrative_division_level_0)
        with self.assertRaises(BadRequestException):
            self.service.add_location(valid_analysis_id, existing_p_code)

    def test_add_location_invalid_analysis_id(self):
        """Tests that adding a location into an unexisting analysis fails"""
        invalid_analysis_id = 2123
        valid_p_code = self.test_administrative_division_level_0.p_code
        with self.assertRaises(NotFoundException):
            self.service.add_location(invalid_analysis_id, valid_p_code)

    def test_remove_location_valid(self):
        """Tests that removing a existing location from a valid analysis works"""
        valid_analysis_id = self.test_analysis.id
        valid_p_code = self.test_administrative_division_level_0.p_code
        self.test_analysis.locations.add(self.test_administrative_division_level_0)

        self.service.remove_location(valid_analysis_id, valid_p_code)
        self.assertNotIn(
            self.test_administrative_division_level_0,
            self.test_analysis.locations.all(),
        )

    def test_remove_location_invalid_p_code(self):
        """Tests that removing a location with a unexisting p_code fails"""
        invalid_p_code = "invalid"
        valid_analysis_id = self.test_analysis.id

        with self.assertRaises(NotFoundException):
            self.service.remove_location(valid_analysis_id, invalid_p_code)

    def test_remove_location_unexisting_p_code(self):
        """Tests that removing a location with an unexisting p_code fails"""
        unexisting_p_code = AdministrativeDivision.objects.create(
            name="existing", p_code="existing", admin_level=0
        ).p_code
        valid_analysis_id = self.test_analysis.id

        with self.assertRaises(BadRequestException):
            self.service.remove_location(valid_analysis_id, unexisting_p_code)

    def test_remove_location_invalid_analysis_id(self):
        """Tests that removing a location into an unexisting analysis fails"""
        invalid_analysis = 32
        existing_p_code = self.test_administrative_division_level_0.p_code

        with self.assertRaises(NotFoundException):
            self.service.remove_location(invalid_analysis, existing_p_code)
