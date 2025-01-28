"""This module contains the tests for the views"""
import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from analysis.models.analysis import Analysis
from analysis.models.analysis_step import AnalysisStep
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.models.sub_pillar import SubPillar
from charts.models import Chart
from common.test_utils import create_logged_in_client, create_test_analysis, create_test_dataset
from file_management.models import ColumnConfiguration
from user_management.models import Organization, Workspace


class AnalysisTestCase(TestCase):
    """TestCase for analysis module"""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(
            title="TestWorkspace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )

    def test_get_analysis_by_id(self):
        """Test if get analysis by id work as expected"""
        analysis = Analysis.objects.create(
            title="test analysis",
            objectives="test",
            end_date="2024-11-20",
            creator_id=self.user.id,
            workspace_id=self.workspace.id,
        )

        response = self.client.get(reverse("get_analysis", args=[analysis.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["payload"]["id"], analysis.id)

    def test_get_analysis_by_id_not_found(self):
        """Test if get analysis by id with an invalid id throw 404"""
        response = self.client.get(reverse("get_analysis", args=[1]))
        self.assertEqual(response.status_code, 404)


class TestGetSteps(TestCase):
    """Test the controller get_steps"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        AnalysisStep.objects.all().delete()
        AnalysisStep.objects.create(name="Test 1", order=1)
        AnalysisStep.objects.create(name="Test 2", order=2)

    def test_get_steps(self):
        """Test that the endpoint retrieves the steps"""
        response = self.client.get(reverse("get_steps"))
        self.assertEqual(response.status_code, 200)
        steps_found = response.data["payload"]
        self.assertEqual(len(steps_found), 2)


class TestGetAnalysisFrameworks(TestCase):
    """Test controller get analysis frameworks"""

    def setUp(self):
        """set up analysis frameworks"""
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_analysis_frameworks_controller")

    def test_get_analysis_frameworks(self):
        """Test that the endpoint retrieves the analysis frameworks"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        analysis_frameworks = response.data["payload"]
        self.assertIsNotNone(analysis_frameworks)


class TestGetAllSectors(TestCase):
    """Test controller get analysis frameworks"""

    def setUp(self):
        """set up analysis frameworks"""
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_analysis_frameworks_controller")

    def test_get_analysis_frameworks(self):
        """Test that the endpoint retrieves the analysis frameworks"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        analysis_frameworks = response.data["payload"]
        self.assertIsNotNone(analysis_frameworks)


class TestCreateOrUpdateAnalysisQuestions(TestCase):
    """Test controller get analysis frameworks"""

    def setUp(self):
        """set up analysis frameworks"""
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(
            title="TestWorkspace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.defaul_step = AnalysisStep.objects.create(
            order=1, name="Test step", mandatory=True
        )
        self.default_analysis = Analysis.objects.create(
            title="test analysis",
            objectives="test",
            end_date="2024-11-20",
            creator_id=self.user.id,
            workspace_id=self.workspace.id,
        )
        self.url = reverse("create_or_update_analysis_question_controller", args=[self.default_analysis.id])

    def test_create_or_update_analysis_question_controller(self):
        """Test that the endpoint retrieves the analysis question"""
        response = self.client.put(self.url, {"content": "question"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["payload"])
        self.assertEqual(response.data['message'], "Analysis question create or updated successfully.")


class TestCreateIssueController(TestCase):
    """Test controller create issue"""

    def setUp(self):
        """set up analysis frameworks"""
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(
            title="TestWorkspace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.defaul_step = AnalysisStep.objects.create(
            order=1, name="Test step", mandatory=True
        )
        self.default_analysis = Analysis.objects.create(
            title="test analysis",
            objectives="test",
            end_date="2024-11-20",
            creator_id=self.user.id,
            workspace_id=self.workspace.id,
        )
        #self.dataset, _ = create_test_dataset(self.user, self.default_analysis)
        #column_config = ColumnConfiguration.objects.first()
        #self.test_subpillar = SubPillar.objects.create(name="test")
        #self.chart = Chart.objects.create(
        #    analysis=self.default_analysis,
        #    name="test",
        #    x_col=column_config,
        #    dataset=None,
        #    subpillar=self.test_subpillar
        #)
        self.data = {
            "name": "testName",
            "description": "testDescription",
            "informationGaps": "testInformationGaps",
            "assumptions": "testAssumptions",
            "disaggregation": 1,
            "entries": [{
                "id": 11,
                "createdAt": "2025-01-17T20:19:00Z",
                "updatedAt": "2025-01-28T00:04:31.754626Z",
                "createdBy": "nayid@dfs.com",
                "fragment": "This Emergency Appeal was launched on 7 June 2012 for CHF 2,537,138 to assist 142,740 beneficiaries (21,960 households) for 9 months.",
                "source": "MDRML009f...",
                "tag": {
                    "id": 40,
                    "name": "1.1. Alignment with population Needs",
                    "alias": None
                }
            }],
            "charts": [],
            "analysisId": 1
        }


        self.url = reverse("create_issue_controller")

    def test_create_issue_controller(self):
        """Test endpoint that creates a new issue"""
        response = self.client.post(self.url, self.data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_issue_controller_400(self):
        """Test endpoint that creates a new issue - Bad Request"""
        self.data["analysisId"] = None
        response = self.client.post(self.url, self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_update_issue_controller(self):
        """Test endpoint that creates a new issue"""
        response = self.client.post(self.url, self.data, content_type="application/json")
        self.data['name'] = "testUpdatedName"
        self.data['entries'] = []
        response = self.client.put(reverse("update_issue_controller",args=[response.data['payload']['id']]), self.data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_issue_controller_404(self):
        """Test endpoint that update an issue - Not Found"""
        self.data['entries'] = []
        response = self.client.put(reverse("update_issue_controller", args=[413]), self.data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_issue_controller(self):
        """Test issue controller retrieves the issues"""
        response = self.client.post(self.url, self.data, content_type="application/json")
        response = self.client.get(reverse("get_issues_controller", args=[self.default_analysis.id]))
        self.assertEqual(response.status_code, 200)


class TestUpdateAnalysisSteps(TestCase):
    """Test the controller update_analysis_steps"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.default_analysis = create_test_analysis(self.user)
        AnalysisStep.objects.all().delete()
        self.defaul_step = AnalysisStep.objects.create(
            order=1, name="Test step", mandatory=True
        )

    def test_update_steps_invalid_analysis_id(self):
        """Test that updating the steps with invalid analysis id raises bad request"""
        response = self.client.put(reverse("update_steps", args=["a"]))
        self.assertEqual(response.status_code, 400)

    def test_update_steps_invalid_data(self):
        """Test that updating the steps with invalid data raises bad request"""
        response = self.client.put(
            reverse("update_steps", args=[self.default_analysis.id]),
            {"invalid_data"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_steps_valid_data(self):
        """Test that updating the steps with valid data works"""
        response = self.client.put(
            reverse("update_steps", args=[self.default_analysis.id]),
            {"step_ids": [self.defaul_step.id]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_analysis_successfully(self):
        """Test that creating an analysis with correct data works"""
        disaggregations = Disaggregation.objects.all()
        sectors = Sector.objects.all()
        response = self.client.post(
            reverse("create_analysis"),
            {
                "title": "Testing creation",
                "disaggregations": [
                    {
                        "id": disaggregations[0].id,
                        "name": disaggregations[0].name
                    }
                ],
                "sectors": [
                    {
                        "id": sectors[0].id,
                        "name": sectors[0].name
                    }
                ],
                "objetives": "This is a test",
                "startDate": "2024-11-25",
                "endDate": "2024-11-29",
                "workspaceId": self.default_analysis.workspace.id,
                "objectives": "objectives",
            }
            , content_type="application/json")

        self.assertEqual(response.status_code, 201)

    # def test_create_analysis_without_sector_error(self):
    #     """Tests that creating an analysis without a sector fails"""
    #     response = self.client.post(
    #         reverse("create_analysis"),
    #         {
    #             "title": "Testing creation",
    #             "disaggregations": [
    #                 "1", "2"
    #             ],
    #             "objetives": "This is a test",
    #             "startDate": "2024-11-25",
    #             "endDate": "2024-11-29"
    #         }
    #     )

    #     self.assertEqual(response.status_code, 400)

    # def test_create_analysis_without_title_error(self):
    #     """Tests that creating an analysis without a title fails"""
    #     response = self.client.post(
    #         reverse("create_analysis"),
    #         {
    #             "disaggregations": [
    #                 "1", "2"
    #             ],
    #             "sectors": [
    #                 "1"
    #             ],
    #             "objetives": "This is a test",
    #             "startDate": "2024-11-25",
    #             "endDate": "2024-11-29"
    #         }
    #     )

    #     self.assertEqual(response.status_code, 400)

    # def test_create_analysis_with_start_date_bigger_than_end_date(self):
    #     """
    #     Tests that creating an analysis with a start date bigger than
    #     the end date fails
    #     """
    #     response = self.client.post(
    #         reverse("create_analysis"),
    #         {
    #             "disaggregations": [
    #                 "1", "2"
    #             ],
    #             "sectors": [
    #                 "1"
    #             ],
    #             "objetives": "This is a test",
    #             "startDate": "2024-11-30",
    #             "endDate": "2024-11-29"
    #         }
    #     )

    #     self.assertEqual(response.status_code, 400)


class TestUploadAnalysisFrameworkCsv(TestCase):
    """Test the controller update analysis framework"""

    def setUp(self):
        self.url = reverse("upload_analysis_framework_controller")
        self.client, self.user = create_logged_in_client()
        self.default_analysis = create_test_analysis(self.user)
        self.csv_filepath = os.path.join(settings.BASE_DIR, 'analysis', 'tests', "ifrc_test.csv")
        self.wrong_format_csv_filepath = os.path.join(settings.BASE_DIR, 'analysis', 'tests',
                                                      "ifrc_wrong_format_test.csv")

    def test_analysis_framework_csv(self):
        """
        Test that uploading a valid CSV file works successfully.
        """
        # Lee el archivo CSV de prueba
        with open(self.csv_filepath, 'rb') as csv_file:
            response = self.client.post(self.url, {'file': csv_file})

        self.assertEqual(response.data['status'], 201)
        self.assertIn("File processed and analysis framework created successfully.", response.data['message'])
        self.assertEqual("ifrc", response.data['payload']['name'])

    def test_analysis_framework_csv_400(self):
        """
        Test that uploading a valid CSV file with wrong format.
        """
        with open(self.wrong_format_csv_filepath, 'rb') as csv_file:
            response = self.client.post(self.url, {'file': csv_file})

        self.assertEqual(response.data['status'], 400)
        self.assertIn('Missing required column: Sub pillar', response.data['message'])
