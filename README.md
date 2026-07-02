# PulseNotify

A simple Django REST API for flight price alerts with JWT auth, Celery background tasks, Redis, and a mock price feed.

## Run locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start Redis:
   ```bash
   docker compose up -d redis
   ```
3. Run the server:
   ```bash
   python manage.py runserver
   ```
4. Run the Celery worker:
   ```bash
   celery -A pulse_notify worker --loglevel=info
   ```
5. Run the Celery beat scheduler:
   ```bash
   celery -A pulse_notify beat --loglevel=info
   ```

## Key endpoints

- POST /api/auth/register/
- POST /api/auth/login/
- GET/POST /api/alerts/
- DELETE /api/alerts/<id>/
- GET /api/flights/price/
- GET /api/admin/summary/

## Tests

```bash
python manage.py test
```
