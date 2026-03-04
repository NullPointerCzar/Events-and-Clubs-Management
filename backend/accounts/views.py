from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom Login View that returns extra user info (name, type)
    alongside the JWT tokens.
    """
    serializer_class = MyTokenObtainPairSerializer

class UserListView(generics.ListCreateAPIView):
    """
    Allows Admin to view all users and create new ones.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Anyone can sign up
    serializer_class = UserSerializer
    

class UserProfileView(APIView):
    # This is the "Gatekeeper"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 'request.user' is automatically populated by the JWT token
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    