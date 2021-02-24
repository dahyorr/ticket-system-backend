from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'Main'
urlpatterns = [
    path('user/login/', obtain_jwt_token, name='Auth Token(POST)'),
]
