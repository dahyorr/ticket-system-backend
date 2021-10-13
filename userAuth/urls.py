from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import RegisterApi, current_user, UserList

app_name = 'userAuth'
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', current_user, name='user'),
    path('users/', UserList.as_view(), name='user List'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterApi.as_view(), name="register user"),
]
