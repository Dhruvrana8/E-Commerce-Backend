from django.urls import path

from authentication.views import LoginAuthenticationView

urlpatterns = [
    path('login/', LoginAuthenticationView.as_view(), name='login'),
]