from django.urls import path

from authentication.views import LoginAuthenticationView, UserRegistrationView

urlpatterns = [
    path('login/', LoginAuthenticationView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
