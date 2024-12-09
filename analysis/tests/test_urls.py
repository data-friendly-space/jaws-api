"""Tests of the urls within analysis"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from analysis.command.load_administrative_divisions import load_administrative_divisions
from analysis.interfaces.controllers.add_location_controller import (
    add_location_controller,
)
from analysis.interfaces.controllers.get_administrative_division_controller import (
    get_administrative_division_controller,
)
from analysis.interfaces.controllers.get_analysis_controller import (
    get_analysis_controller,
)
from analysis.interfaces.controllers.create_analysis_controller import (
    create_analysis_controller,
)
from analysis.interfaces.controllers.get_analysis_by_id_controller import (
    get_analysis_by_id_controller,
)
from analysis.interfaces.controllers.put_analysis_scope_controller import (
    put_analysis_scope_controller,
)
from analysis.interfaces.controllers.remove_location_controller import remove_location_controller


class TestUrls(SimpleTestCase):
    """Contains the tests of each url's controller"""

    def test_get_analyses_url_resolves(self):
        """Test that get analysis url works"""
        url = reverse("get_analyses")
        self.assertEqual(resolve(url).func, get_analysis_controller)

    def test_create_analyses_url_resolves(self):
        """Test that create analysis url works"""
        url = reverse("create_analysis")
        self.assertEqual(resolve(url).func, create_analysis_controller)

    def test_get_analysis_url_resolves(self):
        """Test that get analysis by id works"""
        url = reverse("get_analysis", args=["some-id"])
        self.assertEqual(resolve(url).func, get_analysis_by_id_controller)

    def test_update_analysis_url_resolves(self):
        """Test that the url for updating an analysis works"""
        url = reverse("put_analysis", args=["some-id"])
        self.assertEqual(resolve(url).func, put_analysis_scope_controller)

    def test_load_administrative_divisions_resolves(self):
        """Test that the url for loading divisions works"""
        url = reverse("load_administrative_divisions")
        self.assertEqual(resolve(url).func, load_administrative_divisions)

    def test_get_administrative_divisions_resolves(self):
        """Test that the url for getting the administrative divisions works"""
        url = reverse("get_administrative_divisions")
        self.assertEqual(resolve(url).func, get_administrative_division_controller)

    def test_add_location_resolves(self):
        """Test that the url for adding a location works"""
        url = reverse("add_location", args=['some-analysis-id', 'some-p-code'])
        self.assertEqual(resolve(url).func, add_location_controller)


    def test_remove_location_resolves(self):
        """Test that the url for removing a location works"""
        url = reverse("remove_location", args=["some-analysis-id", "some-p-code"])
        self.assertEqual(resolve(url).func, remove_location_controller)
