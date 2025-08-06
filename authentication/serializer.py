from rest_framework import serializers

class LoginAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


