#!/usr/bin/env python
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from pulse.models import PriceAlert

print("Alert ID=4 detailed check:")
alert = PriceAlert.objects.get(id=4)
print(f"  status field value: '{alert.status}' (repr: {repr(alert.status)})")
print(f"  status == 'active': {alert.status == 'active'}")
print(f"  status == PriceAlert.Status.ACTIVE: {alert.status == PriceAlert.Status.ACTIVE}")

print("\nFiltering for ID=4:")
print(f"  filter(status=PriceAlert.Status.ACTIVE).count(): {PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE).count()}")
found = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE, id=4)
print(f"  filter(status=ACTIVE, id=4).count(): {found.count()}")

if found.count() > 0:
    print("  ✓ Alert found with correct filter")
else:
    print("  ✗ Alert NOT found - checking all alerts:")
    for a in PriceAlert.objects.all():
        print(f"    ID={a.id}: status='{a.status}' (bytes: {a.status.encode()})")

# Test check_prices with detailed logging
print("\n" + "=" * 60)
print("Testing check_prices() with logging:")
print("=" * 60)

active_alerts = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE)
print(f"Active alerts found: {active_alerts.count()}")
for alert in active_alerts:
    print(f"  - {alert.origin}-{alert.destination} (threshold: {alert.threshold_price})")

routes = active_alerts.values_list('origin', 'destination').distinct()
print(f"Distinct routes: {list(routes)}")

for origin, destination in routes:
    route = f'{origin}-{destination}'
    print(f"\nChecking route: {route}")
    try:
        response = requests.get('http://localhost:8000/api/flights/price/', params={'route': route}, timeout=5)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            current_price = data.get('price')
            print(f"  Price: {current_price}")
            
            route_alerts = active_alerts.filter(origin=origin, destination=destination)
            print(f"  Alerts for this route: {route_alerts.count()}")
            for alert in route_alerts:
                should_trigger = current_price <= float(alert.threshold_price)
                print(f"    - Alert ID={alert.id}: {current_price} <= {alert.threshold_price}? {should_trigger}")
    except Exception as e:
        print(f"  Error: {e}")
