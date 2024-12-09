"""Tests Administrative Division model"""
from django.test import TestCase
from ...models.administrative_division import AdministrativeDivision

class AdministrativeDivisionModelTest(TestCase):
    """Wraps all the tests for the administrative division model"""
    def setUp(self):
        self.parent_division = AdministrativeDivision.objects.create(
            country_code="AFG",
            admin_level=1,
            p_code="AF01",
            name="Kabul",
            valid_from_date="2021-11-17"
        )

    def test_create_division_success(self):
        """Tests that creating a division succesfully works well"""
        division = AdministrativeDivision.objects.create(
            country_code="AFG",
            admin_level=2,
            p_code="AF0101",
            name="Paghman",
            parent_p_code=self.parent_division,
            valid_from_date="2021-11-17"
        )
        self.assertEqual(division.name, "Paghman")
        self.assertEqual(division.parent_p_code, self.parent_division)
        self.assertEqual(division.admin_level, 2)

    def test_parent_relationship(self):
        """Tests that the parent relationship of a administrative division is well connected"""
        child_division = AdministrativeDivision.objects.create(
            country_code="AFG",
            admin_level=2,
            p_code="AF0101",
            name="Paghman",
            parent_p_code=self.parent_division,
            valid_from_date="2021-11-17"
        )
        self.assertEqual(child_division.parent_p_code, self.parent_division)
        self.assertIn(child_division, self.parent_division.subdivisions.all())

    def test_unique_p_code(self):
        """Tests that a p-code cannot be duplicated"""
        with self.assertRaises(Exception):
            AdministrativeDivision.objects.create(
                country_code="AFG",
                admin_level=1,
                p_code="AF01",
                name="Duplicate Kabul",
                valid_from_date="2021-11-17"
            )

    def test_str_representation(self):
        """Tests that the str method works return the name and the code"""
        division = AdministrativeDivision.objects.create(
            country_code="AFG",
            admin_level=2,
            p_code="AF0101",
            name="Valid Format",
            valid_from_date="2021-11-17"
        )
        self.assertEqual(str(division), "Valid Format (AF0101)")

    def test_ordering(self):
        """Tests that the ordering works as expected"""
        division1 = AdministrativeDivision.objects.create(
            country_code="AFG",
            admin_level=2,
            p_code="AF0101",
            name="Paghman",
            valid_from_date="2021-11-17"
        )
        divisions = AdministrativeDivision.objects.all()
        self.assertEqual(list(divisions), [self.parent_division, division1])
