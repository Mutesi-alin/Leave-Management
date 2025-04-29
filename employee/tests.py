from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from .models import MonitoringData
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class MonitoringDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="daisychekuiri@gmail.com",
            password="2003rt",
        )

        self.monitoring_data = MonitoringData.objects.create(
            user_id=self.user,
            drainage_id=1,
            water_level=Decimal("10.5"),
            water_pressure=Decimal("2.3"),
            timestamp=timezone.now(),
        )

    def test_monitoring_data_creation(self):
        monitoring_data = MonitoringData.objects.get(
            monitoring_id=self.monitoring_data.monitoring_id
        )
        self.assertEqual(monitoring_data.user_id, self.user)
        self.assertEqual(monitoring_data.drainage_id, 1)
        self.assertEqual(monitoring_data.water_level, Decimal("10.5"))
        self.assertEqual(monitoring_data.water_pressure, Decimal("2.3"))
        self.assertIsInstance(monitoring_data.timestamp, timezone.datetime)

    def test_string_representation(self):
        self.assertEqual(
            str(self.monitoring_data),
            f"Monitoring Data {self.monitoring_data.monitoring_id}",
        )

    def test_monitoring_data_creation_missing_user(self):
        # Unhappy path test: which  Verify's that  IntegrityError is raised if user_id is missing
        with self.assertRaises(IntegrityError):
            MonitoringData.objects.create(
                user_id=None,
                drainage_id=1,
                water_level=Decimal("10.5"),
                water_pressure=Decimal("2.3"),
                timestamp=timezone.now(),
            )

    def test_monitoring_data_creation_missing_drainage_id(self):
        with self.assertRaises(IntegrityError):
            MonitoringData.objects.create(
                user_id=self.user,
                drainage_id=None,
                water_level=Decimal("10.5"),
                water_pressure=Decimal("2.3"),
                timestamp=timezone.now(),
            )

    def test_monitoring_data_creation_invalid_water_level(self):
        monitoring_data = MonitoringData(
            user_id=self.user,
            drainage_id=1,
            water_level=Decimal("-10.5"),
            water_pressure=Decimal("2.3"),
            timestamp=timezone.now(),
        )
        monitoring_data.full_clean()

    def test_monitoring_data_creation_invalid_water_pressure(self):
        # Unhappy path test:  which Verify ValidationError is raised for negative water_pressure

        monitoring_data = MonitoringData(
            user_id=self.user,
            drainage_id=1,
            water_level=Decimal("10.5"),
            water_pressure=Decimal("-2.3"),
            timestamp=timezone.now(),
        )
        monitoring_data.full_clean()

    def test_monitoring_data_creation_missing_timestamp(self):
        MonitoringData.objects.create(
            user_id=self.user,
            drainage_id=1,
            water_level=Decimal("10.5"),
            water_pressure=Decimal("2.3"),
            timestamp=None,
        )
