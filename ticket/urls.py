from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ticket import views

router = DefaultRouter()
router.register('tickets', views.TicketViewSet)
router.register('queues', views.QueueViewSet)
router.register('replies', views.ReplyViewSet)
router.register('notifications', views.NotificationViewSet)
app_name = 'ticket'

urlpatterns = [
    path('', include(router.urls)),
]
