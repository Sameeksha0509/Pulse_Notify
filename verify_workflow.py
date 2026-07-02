#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_notify.settings.local')
django.setup()

from django.contrib.auth.models import User
from pulse.models import PriceAlert, NotificationLog
from pulse.tasks import check_prices
import json

print("=" * 60)
print("CELERY WORKFLOW VERIFICATION TEST")
print("=" * 60)

# Step 1: Get or create test user
print("\n[1] Creating/getting test user...")
user, created = User.objects.get_or_create(
    username='testuser2',
    defaults={'email': 'testuser2@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✓ Created user: {user.username}")
else:
    print(f"✓ User already exists: {user.username}")

# Step 2: Create price alert
print("\n[2] Creating price alert (DEL-BOM, threshold=7000)...")
alert = PriceAlert.objects.create(
    user=user,
    origin='DEL',
    destination='BOM',
    threshold_price=7000,
    status=PriceAlert.Status.ACTIVE
)
print(f"✓ Alert created: ID={alert.id}, Route={alert.origin}-{alert.destination}, Threshold={alert.threshold_price}")

# Step 3: Verify alert in database
print("\n[3] Verifying alert in database...")
alert_check = PriceAlert.objects.get(id=alert.id)
print(f"✓ Alert retrieved: {alert_check.origin}-{alert_check.destination}, Status={alert_check.status}")

# Step 4: Get initial notification count
initial_notifications = NotificationLog.objects.filter(alert=alert).count()
print(f"\n[4] Initial notifications for this alert: {initial_notifications}")

# Step 5: Manually trigger check_prices (simulating beat scheduler)
print("\n[5] Triggering check_prices() task (simulating beat scheduler)...")
print("    With CELERY_TASK_ALWAYS_EAGER=True, this executes synchronously.")
try:
    result = check_prices()
    print(f"✓ check_prices() executed successfully")
except Exception as e:
    print(f"✗ Error executing check_prices(): {e}")
    import traceback
    traceback.print_exc()

# Step 6: Check for new notifications
print("\n[6] Checking for new notifications...")
notifications = NotificationLog.objects.filter(alert=alert).order_by('-notified_at')
new_count = notifications.count()
print(f"✓ Total notifications after task: {new_count}")

if new_count > initial_notifications:
    print("\n[SUCCESS] Notification was created!")
    for notif in notifications[:1]:  # Show most recent
        print(f"   - Notification ID: {notif.id}")
        print(f"   - Triggered Price: {notif.triggered_price}")
        print(f"   - Message: {notif.message}")
        print(f"   - Notified At: {notif.notified_at}")
        
        # Verify alert status was updated
        alert_updated = PriceAlert.objects.get(id=alert.id)
        print(f"   - Alert Status: {alert_updated.status}")
else:
    print("\n[WARNING] No notifications created")
    print("Possible reasons:")
    print("  - Price was not below threshold")
    print("  - No active alerts found")
    print("  - Task encountered an error (check logs above)")

# Step 7: Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"✓ User: {user.username} (ID={user.id})")
print(f"✓ Alert: {alert.origin}-{alert.destination} @ {alert.threshold_price} (ID={alert.id})")
print(f"✓ Notifications Created: {new_count - initial_notifications}")
print(f"✓ Celery Eager Mode: ACTIVE (tasks execute synchronously)")
print("=" * 60)
