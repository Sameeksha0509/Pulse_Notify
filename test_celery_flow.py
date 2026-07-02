import urllib.request, json, time, sys

# Register user
print("=== REGISTERING USER ===")
url = 'http://127.0.0.1:8000/api/auth/register/'
data = json.dumps({'username': 'testuser', 'password': 'testpass123', 'email': 'test@example.com'}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print('REGISTERED:', result['username'])
        token = result['access']
        print('TOKEN:', token[:50] + '...')
except urllib.error.HTTPError as e:
    resp = e.read().decode()
    if 'already exists' in resp:
        print('User already exists, logging in...')
        # Try login
        url = 'http://127.0.0.1:8000/api/auth/login/'
        data = json.dumps({'username': 'testuser', 'password': 'testpass123'}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            token = result['access']
            print('TOKEN:', token[:50] + '...')
    else:
        print('ERROR:', resp)
        sys.exit(1)

# Create alert
print("\n=== CREATING ALERT ===")
url = 'http://127.0.0.1:8000/api/alerts/'
alert_data = json.dumps({
    'origin': 'DEL',
    'destination': 'BOM',
    'threshold_price': 7000
}).encode()
req = urllib.request.Request(url, data=alert_data, headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
})
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print('ALERT CREATED:', result['id'])
        print('Route:', f"{result['origin']}-{result['destination']}")
        print('Threshold:', result['threshold_price'])
        print('Status:', result['status'])
except urllib.error.HTTPError as e:
    print('ERROR:', e.read().decode())
    sys.exit(1)

print("\n=== WAITING FOR CELERY BEAT (60 seconds) ===")
for i in range(60):
    print(f"Wait {i+1}/60...", end='\r')
    time.sleep(1)

print("\n=== CHECKING NOTIFICATIONS ===")
url = 'http://127.0.0.1:8000/api/alerts/'
req = urllib.request.Request(url, headers={
    'Authorization': f'Bearer {token}'
})
try:
    with urllib.request.urlopen(req) as response:
        alerts = json.loads(response.read().decode())
        if alerts:
            alert = alerts[0]
            print('Alert Status:', alert['status'])
            if alert.get('notifications'):
                print('Notifications:', alert['notifications'])
            else:
                print('No notifications yet - check if tasks ran in worker/beat terminals')
        else:
            print('No alerts found')
except Exception as e:
    print('ERROR:', e)
