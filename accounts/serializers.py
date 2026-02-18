from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}} # Don't send password back to React

    def create(self, validated_data):
        # Use create_user to ensure the password gets hashed correctly
        return User.objects.create_user(**validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token['full_name'] = user.full_name
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        # super().validate will now work because user.id exists as a property!
        data = super().validate(attrs)
        
        # Add extra info for the React response
        data['full_name'] = self.user.full_name
        data['user_type'] = self.user.user_type
        data['user_id'] = self.user.user_id
        return data