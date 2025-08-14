from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email= models.EmailField(unique=True)
    phone_number = models.CharField(max_length=35, blank=True, null=True)
    country_code = models.CharField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.username
