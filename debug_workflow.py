#!/usr/bin/env python
import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from pulse.models import PriceAlert, NotificationLog

print("=" * 60)
print("CELERY WORKFLOW DEBUG")
print("=" * 60)

# Test 1: Check if server is running
print("\n[1] Testing if Django server is running...")
try:
    response = requests.get('http://127.0.0.1:8000/api/flights/price/?route=DEL-BOM', timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Server is running!")
        print(f"✓ Price endpoint response: {data}")
        current_price = data.get('price')
        print(f"✓ Current price for DEL-BOM: {current_price}")
    else:
        print(f"✗ Server returned status {response.status_code}")
        sys.exit(1)
except requests.RequestException as e:
    print(f"✗ Cannot connect to server: {e}")
    sys.exit(1)

# Test 2: Get active alerts
print("\n[2] Fetching active alerts...")
active_alerts = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE)
print(f"✓ Active alerts: {active_alerts.count()}")
for alert in active_alerts:
    print(f"  - Alert ID={alert.id}: {alert.origin}-{alert.destination}, threshold={alert.threshold_price}")

# Test 3: Check price threshold
print("\n[3] Checking if price <= threshold...")
for alert in active_alerts.filter(origin='DEL', destination='BOM'):
    print(f"  - Current price: {current_price}")
    print(f"  - Alert threshold: {alert.threshold_price}")
    print(f"  - Price <= Threshold? {current_price <= float(alert.threshold_price)}")
    
    if current_price <= float(alert.threshold_price):
        print(f"  ✓ SHOULD TRIGGER!")
    else:
        print(f"  ✗ Will NOT trigger (price above threshold)")

# Test 4: Manual notification creation
print("\n[4] Manually creating notification for debugging...")
alert = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE, origin='DEL', destination='BOM').first()
if alert:
    message = f'Price alert triggered! {alert.origin}-{alert.destination} is now ₹{current_price} - below your threshold of ₹{alert.threshold_price}'
    notif = NotificationLog.objects.create(
        alert=alert,
        triggered_price=current_price,
        message=message,
    )
    print(f"✓ Manually created notification ID={notif.id}")
    print(f"  - Message: {notif.message}")
    
    # Update alert status
    alert.status = PriceAlert.Status.TRIGGERED
    alert.save()
    print(f"✓ Updated alert status to TRIGGERED")
else:
    print(f"✗ No active DEL-BOM alert found")

# Test 5: Verify in database
print("\n[5] Verifying notifications in database...")
notifs = NotificationLog.objects.all().order_by('-notified_at')[:1]
if notifs:
    notif = notifs[0]
    print(f"✓ Most recent notification:")
    print(f"  - ID: {notif.id}")
    print(f"  - Alert: {notif.alert.origin}-{notif.alert.destination}")
    print(f"  - Price: ₹{notif.triggered_price}")
    print(f"  - Message: {notif.message}")
    print(f"  - Time: {notif.notified_at}")
