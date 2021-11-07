from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, UserListSerializer
from rest_framework.decorators import api_view
from .models import User


class RegisterApi(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user,    context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Please Login",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(generics.ListAPIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        authorized = self.request.query_params.get('authorized')
        if authorized and bool(int(authorized)):
            queryset = queryset.filter(is_authorized=True)

        return queryset.all()
