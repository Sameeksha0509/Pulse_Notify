#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from pulse.models import PriceAlert

print("Checking status enum values:")
print(f"PriceAlert.Status.ACTIVE = '{PriceAlert.Status.ACTIVE}'")
print(f"PriceAlert.Status.INACTIVE = '{PriceAlert.Status.INACTIVE}'")
print(f"PriceAlert.Status.TRIGGERED = '{PriceAlert.Status.TRIGGERED}'")

print("\nAlert ID=3 status check:")
alert = PriceAlert.objects.get(id=3)
print(f"alert.status = '{alert.status}' (type: {type(alert.status).__name__})")
print(f"alert.status == 'ACTIVE': {alert.status == 'ACTIVE'}")
print(f"alert.status == 'active': {alert.status == 'active'}")
print(f"alert.status == PriceAlert.Status.ACTIVE: {alert.status == PriceAlert.Status.ACTIVE}")

print("\nFiltering test:")
print(f"PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE).count() = {PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE).count()}")
print(f"PriceAlert.objects.filter(status='active').count() = {PriceAlert.objects.filter(status='active').count()}")
print(f"PriceAlert.objects.filter(status='ACTIVE').count() = {PriceAlert.objects.filter(status='ACTIVE').count()}")
