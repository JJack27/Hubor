from django.urls import path
from notification.consumer import NotificationConsumer

websocket_urlpatterns = [
    path('notification/<int:room_number>/', NotificationConsumer),
]