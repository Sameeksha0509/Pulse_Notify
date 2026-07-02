from django.urls import path

from .views import (
    admin_summary_view,
    alerts_view,
    delete_alert_view,
    flight_price_view,
    login_view,
    register_view,
)

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('alerts/', alerts_view, name='alerts'),
    path('alerts/<int:alert_id>/', delete_alert_view, name='delete-alert'),
    path('flights/price/', flight_price_view, name='flight-price'),
    path('admin/summary/', admin_summary_view, name='admin-summary'),
]
