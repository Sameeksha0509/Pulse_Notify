import random
from decimal import Decimal

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import NotificationLog, PriceAlert
from .permissions import IsAdminUser

MOCK_PRICES = {
    'DEL-BOM': (3000, 7000),
    'BLR-HYD': (1500, 4000),
    'DEL-BLR': (4000, 9000),
    'BOM-GOA': (2000, 5000),
}


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    profile = user.profile
    refresh = RefreshToken.for_user(user)
    return Response({
        'username': user.username,
        'access': str(refresh.access_token),
        'role': profile.role,
    }, status=201)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token)})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def alerts_view(request):
    if request.method == 'GET':
        alerts = PriceAlert.objects.filter(user=request.user)
        data = [{
            'id': alert.id,
            'origin': alert.origin,
            'destination': alert.destination,
            'threshold_price': float(alert.threshold_price),
            'status': alert.status,
        } for alert in alerts]
        return Response(data)

    origin = request.data.get('origin')
    destination = request.data.get('destination')
    threshold_price = request.data.get('threshold_price')

    if not origin or not destination or not threshold_price:
        return Response({'error': 'origin, destination, and threshold_price are required'}, status=400)

    alert = PriceAlert.objects.create(
        user=request.user,
        origin=origin.upper(),
        destination=destination.upper(),
        threshold_price=Decimal(str(threshold_price)),
    )
    return Response({
        'id': alert.id,
        'origin': alert.origin,
        'destination': alert.destination,
        'threshold_price': float(alert.threshold_price),
        'status': alert.status,
    }, status=201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_alert_view(request, alert_id):
    alert = get_object_or_404(PriceAlert, id=alert_id)
    if alert.user != request.user:
        return Response(status=404)

    alert.status = PriceAlert.Status.INACTIVE
    alert.save()
    return Response({'status': 'inactive'})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def flight_price_view(request):
    route = request.GET.get('route', '')
    price_range = MOCK_PRICES.get(route)
    if not price_range:
        return JsonResponse({'error': 'Route not found'}, status=404)
    price = random.randint(*price_range)
    return JsonResponse({'route': route, 'price': price})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_summary_view(request):
    total_alerts = PriceAlert.objects.aggregate(total_alerts=models.Count('id'))['total_alerts']
    active_alerts = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE).count()
    triggered_alerts = PriceAlert.objects.filter(status=PriceAlert.Status.TRIGGERED).count()
    total_notifications = NotificationLog.objects.count()
    top_routes = list(
        PriceAlert.objects.values('origin', 'destination').annotate(alert_count=models.Count('id')).order_by('-alert_count')[:5]
    )
    return Response({
        'total_alerts': total_alerts,
        'active_alerts': active_alerts,
        'triggered_alerts': triggered_alerts,
        'total_notifications': total_notifications,
        'top_routes': [
            {
                'route': f"{item['origin']}-{item['destination']}",
                'alert_count': item['alert_count'],
            }
            for item in top_routes
        ],
    })
