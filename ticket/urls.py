from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ticket import views

router = DefaultRouter()
router.register('queues', views.QueueViewSet)
router.register('tickets', views.TicketViewSet)
app_name = 'ticket'

urlpatterns = [
    path('', include(router.urls))
]
