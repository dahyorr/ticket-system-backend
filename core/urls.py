from django.urls import path
from .views import current_user, UserList

urlpatterns = [
    path('auth/user/current/', current_user),
    path('auth/user/new/', UserList.as_view(), name='Create New User(POST)')
]