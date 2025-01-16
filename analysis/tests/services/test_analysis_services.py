"""Contains the tests for analysis service"""

from django.test import TestCase

from analysis.contract.to.administrative_division_to import AdministrativeDivisionTO
from analysis.contract.to.analysis_framework_to import AnalysisFrameworkTO
from analysis.contract.to.analysis_question_to import AnalysisQuestionTO
from analysis.contract.to.disaggregation_to import DisaggregationTO
from analysis.contract.to.sector_to import SectorTO
from analysis.interfaces.serializers.administrative_division_serializer import (
    AdministrativeDivisionSerializer,
)
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.analysis_framework import AnalysisFramework
from analysis.models.analysis_question import AnalysisQuestion
from analysis.models.analysis_step import AnalysisStep
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException, NotFoundException
from common.helpers.query_options import QueryOptions
from common.test_utils import create_logged_in_client, create_test_analysis, create_test_organization
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

        self.test_sector = Sector.objects.get(id=1)
        self.test_disaggregation = Disaggregation.objects.get(id=1)
        self.test_administrative_division_level_0 = AdministrativeDivision.objects.create(
            p_code="test", name="Test", admin_level=0
        )
        self.test_analysis = Analysis.objects.create(
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

    def test_get_sectors_with_valid_sectors(self):
        """Tests that get sectors with valid sectors works"""
        sectors = self.service.get_all_sectors(pk__in=[1])
        self.assertEqual(SectorTO.from_model(self.test_sector).to_dict(), sectors[0])

    def test_get_disaggregations_with_valid_disaggregations(self):
        """Tests that get disaggregations with valid disaggregations works"""
        disaggregations = self.service.get_disaggregations([1])
        self.assertEqual(DisaggregationTO.from_model(self.test_disaggregation).to_dict(), disaggregations[0])

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


class TestGetSteps(TestCase):
    """Test that getting steps and mandatory steps work"""

    def setUp(self):
        AnalysisStep.objects.all().delete()
        self.default_step = AnalysisStep.objects.create(name="Test 1", order=1)
        AnalysisStep.objects.create(name="Test 2", order=2)

        self.service = AnalysisServiceImpl()

    def test_get_steps(self):
        """Test that getting the steps works correctly"""
        steps = self.service.get_steps()
        self.assertEqual(len(steps), 2)

    def test_get_mandatory_steps(self):
        """Test that getting the mandatory steps works correctly"""
        AnalysisStep.objects.create(
            name="Not mandatory", order=1, step_parent=self.default_step
        )
        all_steps = self.service.get_steps()
        mandatory_steps = self.service.get_mandatory_step_ids()
        self.assertEqual(len(all_steps), 3)
        self.assertEqual(len(mandatory_steps), 2)


class TestUpdateAnalysisSteps(TestCase):
    """Test that updating some analysis's steps works as expected"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.service = AnalysisServiceImpl()
        AnalysisStep.objects.all().delete()
        mandatory_step_1 = AnalysisStep.objects.create(name="Mandatory 1", order=1)
        mandatory_step_2 = AnalysisStep.objects.create(name="Mandatory 2", order=2)
        self.mandatory_step_ids = [mandatory_step_1.id, mandatory_step_2.id]
        not_required_steps = [
            {"name": "Not required 1", "order": 1, "step_parent": mandatory_step_1},
            {"name": "Not required 2", "order": 2, "step_parent": mandatory_step_1},
        ]
        self.not_required_step_1 = AnalysisStep.objects.create(**not_required_steps[0])
        self.not_required_step_2 = AnalysisStep.objects.create(**not_required_steps[1])

    def test_invalid_analysis_id_fails(self):
        """Test that updating an analysis steps with invalid analysis id fails"""
        invalid_analysis_id = 3
        valid_step_ids = self.mandatory_step_ids
        with self.assertRaises(NotFoundException):
            self.service.update_steps(invalid_analysis_id, valid_step_ids)

    def test_no_step_ids(self):
        """Test that updating an analysis steps without steps fails"""
        valid_analysis_id = self.analysis.id
        invalid_steps = []
        with self.assertRaises(BadRequestException):
            self.service.update_steps(valid_analysis_id, invalid_steps)

    def test_wrong_step_ids(self):
        """Test that using wrong analysis step fails"""
        valid_analysis_id = self.analysis.id
        invalid_steps = [83]
        with self.assertRaises(BadRequestException):
            self.service.update_steps(valid_analysis_id, invalid_steps)

    def test_mandatory_steps_missing(self):
        """Test that omitting the mandatory steps fails"""
        valid_analysis_id = self.analysis.id
        invalid_steps = [self.mandatory_step_ids[0]]
        with self.assertRaises(BadRequestException):
            self.service.update_steps(valid_analysis_id, invalid_steps)

    def test_valid_analysis_and_valid_steps(self):
        """Test that updating an analysis steps with valid steps works"""
        valid_analysis_id = self.analysis.id
        valid_step_ids = self.mandatory_step_ids.copy()
        valid_step_ids.append(self.not_required_step_1.id)
        valid_step_ids.append(self.not_required_step_2.id)

        # Update the analysis steps
        self.service.update_steps(valid_analysis_id, valid_step_ids)

        # Validate new ids
        new_step_ids = [step.id for step in self.analysis.analysis_steps.all()]

        self.assertEqual(valid_step_ids, new_step_ids)


class TestGetAnalysisFrameworks(TestCase):
    """Test that get analysis's frameworks works as expected"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = AnalysisServiceImpl()

    def test_get_analysis_frameworks(self):
        analysis_frameworks = self.service.get_all_analysis_frameworks(QueryOptions())
        self.assertIsNotNone(analysis_frameworks)


class TestGetAllSectors(TestCase):
    """Test that get all sectors works as expected"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = AnalysisServiceImpl()

    def test_get_all_sectors(self):
        sectors = self.service.get_all_sectors()
        self.assertIsNotNone(sectors)


class TestAssignOrUpdateAnalysisFramework(TestCase):
    """Test that get all sectors works as expected"""

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
        self.analysis = Analysis.objects.create(
            title="TestAnalysis15",
            workspace_id=self.workspace.id,
            end_date="2024-12-17",
            creator_id=self.user.id,
        )

    def test_create_or_update_analysis_framework(self):
        analysis_updated = self.service.update_analysis_framework(self.analysis.id, 1)
        analysisFramework = AnalysisFramework.objects.get(id=1)
        self.assertIsNotNone(analysis_updated)
        self.assertEqual(analysis_updated['analysisFramework'], AnalysisFrameworkTO.from_model(analysisFramework).to_dict())


class TestCreateOrUpdateAnalysisQuestion(TestCase):
    """Test that get all sectors works as expected"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = AnalysisServiceImpl()
        self.org = Organization.objects.create(name="TestOrganization4")
        self.workspace = Workspace.objects.create(
            title="TestWorksp2ace12",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.analysis = Analysis.objects.get_or_create(
            title="TestAnalysis16",
            workspace_id=self.workspace.id,
            end_date="2024-12-17",
            creator_id=self.user.id,
        )

    def test_create_or_update_analysis_question(self):
        analysis_question_updated = self.service.update_analysis_questions(self.analysis[0].id, "question test")
        analysis_question = AnalysisQuestion.objects.get(analysis_id=self.analysis[0].id)
        self.assertIsNotNone(analysis_question_updated)
        self.assertEqual(analysis_question_updated,AnalysisQuestionTO.from_model(analysis_question).to_dict())



