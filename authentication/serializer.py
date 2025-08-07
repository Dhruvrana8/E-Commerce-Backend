from rest_framework import serializers
from django.contrib.auth.models import User

class LoginAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields ="__all__"

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"Password Error": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            **validated_data
        )
        return user
