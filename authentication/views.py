from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from authentication.serializer import LoginAuthenticationSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

class LoginAuthenticationView(APIView):
    def post(self, request):
        # We need to check if the user has entered the Username and Password, or not
        password = request.data.get('password')
        username = request.data.get('username')
        if not username or not password:
            return Response({'Error': 'Username and Password are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        serializer = LoginAuthenticationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = authenticate(username=username, password=password)
        # In case the username or the password is not correct, we need to send the bad request error
        if not user_obj:
            return Response({'Error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user_obj)
        return Response({
            "Token": str(token),
        }, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        username = request.data.get('username')
        password = request.data.get('password')
        if not first_name or not username or not password:
            return Response({"Error": "Username, Password and Firstname are required fields"},
                            status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        serialize = UserRegistrationSerializer(data=data)
        if not serialize.is_valid():
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = serialize.save()
        token, _ = Token.objects.get_or_create(user=user_obj)
        return Response({
            "Token": str(token),
            "Message": "The User has been registered successfully."
        })

