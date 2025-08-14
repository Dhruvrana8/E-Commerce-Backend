from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_verified', 'date_joined',
                  'address', 'phone_number', 'pincode', 'country', 'country_code']
        read_only_fields = ['username', 'is_verified']  # user cannot change username or verification status
