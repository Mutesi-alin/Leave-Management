from django.test import TestCase
from .models import Sensor
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class SensorModelTest(TestCase):
    def setUp(self):
        self.sensor = Sensor.objects.create(
            Type="Waterpressure",
            Location="Nairobi",
            Status="Active",
            Time_Date=timezone.now().date(),
        )

    def test_sensor_creation(self):
        sensor = Sensor.objects.get(Sensor_ID=self.sensor.Sensor_ID)
        self.assertEqual(sensor.Type, "Waterpressure")
        self.assertEqual(sensor.Location, "Nairobi")
        self.assertEqual(sensor.Status, "Active")
        self.assertEqual(sensor.Time_Date, self.sensor.Time_Date)

    def test_sensor_string_representation(self):
        self.assertEqual(
            str(self.sensor), f"Sensor {self.sensor.Sensor_ID} - Waterpressure"
        )

    def test_default_location(self):
        default_sensor = Sensor.objects.create(Type="Water Pressure", Status="Inactive")
        self.assertEqual(default_sensor.Location, "karen")

    def test_sensor_creation_missing_type(self):
        with self.assertRaises(IntegrityError):
            Sensor.objects.create(Type=None, Location="Karen", Status="Active")

    def test_sensor_creation_missing_status(self):
        with self.assertRaises(IntegrityError):
            Sensor.objects.create(Type="Waterpressure", Location="Nasra", Status=None)

    def test_sensor_creation_invalid_location(self):
        with self.assertRaises(ValidationError):
            sensor = Sensor(
                Type="Waterpressure", Location="Karen" * 300, Status="Active"
            )
            sensor.full_clean()

    def test_sensor_creation_invalid_type(self):
        with self.assertRaises(ValidationError):
            sensor = Sensor(Type="waterlevel" * 300, Location="Nasra", Status="Active")
            sensor.full_clean()
