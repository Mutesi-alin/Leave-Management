from django.test import TestCase
from .models import DrainageSystem
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone


class DrainageSystemModelTest(TestCase):
    def setUp(self):
        self.drainage_system = DrainageSystem.objects.create(
            Location="Karen", waterlevel=5.75, waterpressure=4.45, Status="Active"
        )

    def test_drainage_system_creation(self):
        drainage_system = DrainageSystem.objects.get(
            Drainage_ID=self.drainage_system.Drainage_ID
        )
        self.assertEqual(drainage_system.Location, "Karen")
        self.assertEqual(drainage_system.waterlevel, 5.75)
        self.assertEqual(drainage_system.Status, "Active")
        self.assertIsNotNone(drainage_system.Timestamp)

    def test_drainage_system_string_representation(self):
        self.assertEqual(
            str(self.drainage_system),
            f"Drainagesystem {self.drainage_system.Drainage_ID}",
        )

    def test_drainage_system_creation_missing_location(self):
        with self.assertRaises(IntegrityError):
            DrainageSystem.objects.create(
                Location=None, waterlevel=5.75, waterpressure=3.45, Status="Active"
            )

    def test_drainage_system_creation_missing_waterlevel(self):
        with self.assertRaises(IntegrityError):
            DrainageSystem.objects.create(
                Location="Karen", waterlevel=None, waterpressure=3.45, Status="Active"
            )

    def test_drainage_system_creation_missing_waterpressure(self):
        with self.assertRaises(IntegrityError):
            DrainageSystem.objects.create(
                Location="Karen", waterlevel=5.75, waterpressure=None, Status="Active"
            )

    def test_drainage_system_creation_missing_status(self):
        with self.assertRaises(IntegrityError):
            DrainageSystem.objects.create(
                Location="Karen", waterlevel=5.75, waterpressure=3.45, Status=None
            )

    def test_invalid_waterlevel(self):
        drainage_system = DrainageSystem(
            Location="Karen", waterlevel=-5.75, waterpressure=3.45, Status="Active"
        )
        with self.assertRaises(ValidationError):
            drainage_system.full_clean()

    def test_invalid_waterpressure(self):
        drainage_system = DrainageSystem(
            Location="Karen", waterlevel=5.75, waterpressure=-3.45, Status="Active"
        )
        with self.assertRaises(ValidationError):
            drainage_system.full_clean()

    def test_long_location(self):
        long_location = "x" * 200
        drainage_system = DrainageSystem(
            Location=long_location, waterlevel=5.75, waterpressure=3.45, Status="Active"
        )
        with self.assertRaises(ValidationError):
            drainage_system.full_clean()
