from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tickets/', consumers.TicketConsumer.as_asgi()),
]
