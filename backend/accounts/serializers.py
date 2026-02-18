from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Using the standard 'id' now!
        fields = ['id', 'full_name', 'email', 'user_type', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # This is crucial: it uses the UserManager we wrote in models.py 
        # to hash the password properly.
        return User.objects.create_user(**validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # These are encoded INSIDE the token (good for security checks)
        token['full_name'] = user.full_name
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        # This executes the standard login check
        data = super().validate(attrs)

        # This adds plain text data to the JSON response 
        # (easy for React to read without decoding the JWT)
        data['full_name'] = self.user.full_name
        data['user_type'] = self.user.user_type
        data['id'] = self.user.id
        
        return data