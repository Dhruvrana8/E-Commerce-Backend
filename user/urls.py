from django.urls import path

from user.views import UserProfileView

urlpatterns = [
    path('', UserProfileView.as_view(), name='user_profile'),
]