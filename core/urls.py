from django.urls import path
from .views import current_user, UserCreate

urlpatterns = [
    path('auth/user/', current_user),
    path('auth/user/create/', UserCreate.as_view(), name='Create New User(POST)')
]