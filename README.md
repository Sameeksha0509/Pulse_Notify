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
<img width="527" height="403" alt="Register_User" src="https://github.com/user-attachments/assets/8c04b307-d6f6-4c1d-bb29-8375bd6c91ba" />
<img width="535" height="334" alt="Register_Duplicate_User" src="https://github.com/user-attachments/assets/03fcd786-a1d2-4ecc-9cde-b2a17c29e99a" />
<img width="530" height="356" alt="Mock_Price_Feed_(Valid Route)-Example1" src="https://github.com/user-attachments/assets/ab1e4c0f-96e9-4a6e-98fa-2fa41f37a2e0" />
<img width="529" height="346" alt="Mock_Price_Feed(Valid Route)-Example3" src="https://github.com/user-attachments/assets/3b8f7942-3b1a-456e-9d7e-fa5c9150f93f" />
<img width="527" height="369" alt="Mock_Price_Feed(Valid Route)-Example2" src="https://github.com/user-attachments/assets/c3b2724b-4f5c-4a90-a925-319ce9918012" />
<img width="527" height="347" alt="Mock_Price_Feed (Invalid Route)" src="https://github.com/user-attachments/assets/c43801af-e0f6-4336-ac9a-0f9f1d002728" />
<img width="529" height="370" alt="Login_with_wrong_password" src="https://github.com/user-attachments/assets/03e6c139-61ee-4014-845f-77fe73ab4416" />
<img width="533" height="377" alt="Login_with_valid_credentials" src="https://github.com/user-attachments/assets/54d39e19-f311-42f8-b4f0-d236aec62fa7" />
<img width="536" height="414" alt="List_Own_Alerts" src="https://github.com/user-attachments/assets/56d2c4b4-84e3-49f1-9f07-6426c2e4e20a" />
<img width="530" height="362" alt="Deactivate_Alert" src="https://github.com/user-attachments/assets/43c866fb-ffca-42c3-a87c-66d6ce8336e6" />
<img width="536" height="334" alt="Create_Price_Alert(WITHOUT Token)" src="https://github.com/user-attachments/assets/657317ef-949d-482c-b2a9-5021125576ca" />
<img width="538" height="377" alt="Create_Price_Alert(With Token)" src="https://github.com/user-attachments/assets/1e05b62c-636b-4377-9cab-07f34cd059a0" />
<img width="530" height="338" alt="Admin_Summary_(Regular User)" src="https://github.com/user-attachments/assets/164ae14f-97f8-48a8-b01e-78298e009bd8" />
<img width="536" height="431" alt="Admin_Summary(Admin Token)" src="https://github.com/user-attachments/assets/db3b3244-66e7-434e-a1ee-604326065000" />
<img width="745" height="160" alt="image" src="https://github.com/user-attachments/assets/3e669f10-9fa5-4a07-9e95-1e04a6b2cf67" />
