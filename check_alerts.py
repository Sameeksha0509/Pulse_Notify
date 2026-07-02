#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from pulse.models import PriceAlert

print("All Alerts in Database:")
print("=" * 80)
alerts = PriceAlert.objects.all()
for alert in alerts:
    print(f"ID={alert.id}, User={alert.user.username}, Route={alert.origin}-{alert.destination}, "
          f"Threshold={alert.threshold_price}, Status={alert.status}")

print("\n" + "=" * 80)
print(f"Total alerts: {alerts.count()}")
print(f"Active alerts: {PriceAlert.objects.filter(status='ACTIVE').count()}")
print(f"Triggered alerts: {PriceAlert.objects.filter(status='TRIGGERED').count()}")
print(f"Inactive alerts: {PriceAlert.objects.filter(status='INACTIVE').count()}")
