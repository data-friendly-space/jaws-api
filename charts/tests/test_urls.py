"""Contain the tests for the urls"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from charts.interfaces.controllers.get_charts_controller import get_charts_controller
from charts.interfaces.controllers.save_chart_controller import save_chart_controller


class TestUrls(SimpleTestCase):
    """Test each url"""
    def test_save_charts(self):
        """Test that the url for saving a chart works"""
        url = reverse("save")
        self.assertEqual(resolve(url).func, save_chart_controller)

    def test_get_charts(self):
        """Test that the url for getting the charts works"""
        url = reverse("get_charts")
        self.assertEqual(resolve(url).func, get_charts_controller)
