#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from pulse.models import PriceAlert

print("Fixing status values in database...")
print("\nBefore fix:")
for alert in PriceAlert.objects.all():
    print(f"  ID={alert.id}: status='{alert.status}'")

# Fix uppercase statuses
updated_count = 0
for alert in PriceAlert.objects.all():
    if alert.status == 'ACTIVE':
        alert.status = PriceAlert.Status.ACTIVE
        alert.save()
        updated_count += 1
        print(f"Fixed ID={alert.id}: 'ACTIVE' → '{PriceAlert.Status.ACTIVE}'")
    elif alert.status == 'INACTIVE':
        alert.status = PriceAlert.Status.INACTIVE
        alert.save()
        updated_count += 1
        print(f"Fixed ID={alert.id}: 'INACTIVE' → '{PriceAlert.Status.INACTIVE}'")
    elif alert.status == 'TRIGGERED':
        alert.status = PriceAlert.Status.TRIGGERED
        alert.save()
        updated_count += 1
        print(f"Fixed ID={alert.id}: 'TRIGGERED' → '{PriceAlert.Status.TRIGGERED}'")

print(f"\nTotal fixed: {updated_count}")

print("\nAfter fix:")
for alert in PriceAlert.objects.all():
    print(f"  ID={alert.id}: status='{alert.status}'")

print("\nFiltering test:")
active = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE).count()
inactive = PriceAlert.objects.filter(status=PriceAlert.Status.INACTIVE).count()
triggered = PriceAlert.objects.filter(status=PriceAlert.Status.TRIGGERED).count()
print(f"Active: {active}, Inactive: {inactive}, Triggered: {triggered}")
