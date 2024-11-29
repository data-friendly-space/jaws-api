'''This module contains the tests for the views'''
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.models.analysis import Analysis
from user_management.models.user import User

# Create your tests here.


class AnalysisTestCase(TestCase):
    '''TestCase for analysis module'''
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        user = User.objects.create(
            name="TestName",
            lastname="TestLastname",
            email="test@test.com",
            password="testpassword"
        )
        refresh = RefreshToken.for_user(user)
        self.client = Client()
        self.client.force_login(user)
        self.access_token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'

    def test_get_analyses(self):
        '''Test if the get analysis work as expected'''
        response = self.client.get(reverse("get_analyses"))
        self.assertEqual(response.status_code, 200)

    def test_get_analysis_by_id(self):
        '''Test if get analysis by id work as expected'''
        Analysis.objects.create(
            id="test",
            title="test analysis",
            objetives="test",
            end_date="2024-11-20"
        )

        response = self.client.get(reverse("get_analysis", args=["test"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["payload"]["id"], "test")

    def test_get_analysis_by_id_not_found(self):
        '''Test if get analysis by id with an invalid id throw 400'''
        response = self.client.get(reverse("get_analysis", args=["test"]))
        self.assertEqual(response.status_code, 400)

    # def test_create_analysis_successfully(self):
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
