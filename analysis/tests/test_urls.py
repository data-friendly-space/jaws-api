from django.test import SimpleTestCase
from django.urls import reverse, resolve
from analysis.interfaces.controllers.get_analysis_controller import get_analysis_controller
from analysis.interfaces.controllers.create_analysis_controller import create_analysis_controller
from analysis.interfaces.controllers.get_analysis_by_id_controller import get_analysis_by_id_controller


class TestUrls(SimpleTestCase):

    def test_get_analyses_url_resolves(self):
        url = reverse("get_analyses")
        self.assertEqual(resolve(url).func, get_analysis_controller)

    def test_create_analyses_url_resolves(self):
        url = reverse("create_analysis")
        self.assertEqual(resolve(url).func, create_analysis_controller)

    def test_get_analysis_url_resolves(self):
        url = reverse("get_analysis", args=["some-id"])
        self.assertEqual(resolve(url).func, get_analysis_by_id_controller)
