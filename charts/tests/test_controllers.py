"""Contains the test for the controllers"""

from django.test import TestCase
from django.urls import reverse
from moto import mock_aws

from analysis.models.sub_pillar import SubPillar
from charts.models.chart import Chart
from common.test_utils import create_logged_in_client, create_test_analysis, create_test_dataset
from file_management.models.column_configuration import ColumnConfiguration

@mock_aws
class TestGetCharts(TestCase):
    """Test that the endpoint for getting the charts works"""
    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, _ = create_test_dataset(self.user, self.analysis)
        self.test_subpillar = SubPillar.objects.create(name="test")
        self.url = reverse("get_charts")

    def test_no_analysis_id(self):
        """Test that if the analysis id is not provided it returns a bad request"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_no_charts_created(self):
        """Test that if no charts were created it returns 404"""
        response = self.client.get(f"{self.url}?analysis_id={self.analysis.id}")

        self.assertEqual(response.status_code, 404)

    def test_get_chart_found(self):
        """Test that if a chart is found its returned correctly"""
        column_config = ColumnConfiguration.objects.first()
        chart = Chart.objects.create(
            analysis=self.analysis,
            name="test",
            x_col=column_config,
            dataset=self.dataset,
            subpillar=self.test_subpillar
        )

        response = self.client.get(f"{self.url}?analysis_id={self.analysis.id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        self.assertTrue(isinstance(response.data["payload"], list), "The response must be a list")
        self.assertIn("name", response.data["payload"][0])
        self.assertEqual(chart.name, response.data["payload"][0]["name"])

    def test_get_chart_subpillar_filters(self):
        """Test that the filter by subpillars works"""
        column_config = ColumnConfiguration.objects.first()
        Chart.objects.create(
            analysis=self.analysis,
            name="test",
            x_col=column_config,
            dataset=self.dataset,
            subpillar=self.test_subpillar
        )
        other_subpillar = SubPillar.objects.create(name="subpillar2")
        chart_to_be_found = Chart.objects.create(
            analysis=self.analysis,
            name="test",
            x_col=column_config,
            dataset=self.dataset,
            subpillar=other_subpillar
        )

        response = self.client.get(
            f"{self.url}?analysis_id={self.analysis.id}&subpillar_ids={other_subpillar.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        self.assertTrue(isinstance(response.data["payload"], list), "The response must be a list")
        self.assertEqual(len(response.data["payload"]), 1)
        self.assertIn("name", response.data["payload"][0])
        self.assertEqual(chart_to_be_found.name, response.data["payload"][0]["name"])
