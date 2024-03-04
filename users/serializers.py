import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'full_name', 'avatar')
        extra_kwargs = {
            'full_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_full_name(self, value):
        # Check if full_name contains special symbols
        if not re.match(r'^[a-zA-Z0-9 ]+$', value):
            raise serializers.ValidationError("Full name can't contain special symbols.")

        # Check if full_name has minimum length of 3 characters
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")

        return value

    def validate_avatar(self, value):
        # Check if avatar format is valid
        valid_formats = ['image/png', 'image/jpeg', 'image/jpg']
        if value.content_type not in valid_formats:
            raise serializers.ValidationError("Avatar must be in PNG, JPG, or JPEG format.")

        return value
    
    def validate_password(self, value):
        # Use Django's default password validation
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            avatar=validated_data.get('avatar')  # Include the avatar field if provided
        )
        return user
