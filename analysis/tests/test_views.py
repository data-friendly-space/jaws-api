"""This module contains the tests for the views"""
from django.test import TestCase
from django.urls import reverse

from analysis.models.analysis import Analysis
from common.test_utils import create_logged_in_client
from user_management.models import Organization, Workspace


class AnalysisTestCase(TestCase):
    """TestCase for analysis module"""


    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(title="TestWorkspace1", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)

    def test_get_analysis_by_id(self):
        """Test if get analysis by id work as expected"""

        Analysis.objects.create(
            id=1,
            title="test analysis",
            objectives="test",
            end_date="2024-11-20",
            creator_id=self.user.id,
            workspace_id= self.workspace.id
        )

        response = self.client.get(reverse("get_analysis", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["payload"]["id"], 1)

    def test_get_analysis_by_id_not_found(self):
        """Test if get analysis by id with an invalid id throw 404"""
        response = self.client.get(reverse("get_analysis", args=[1]))
        self.assertEqual(response.status_code, 404)

    # def test_create_analysis_successfully(self):
    #     """Test that creating an analysis with correct data works"""
    #     response = self.client.post(
    #         reverse("create_analysis"),
    #         {
    #             "title": "Testing creation",
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

    #     self.assertEqual(response.status_code, 201)

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