from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    job = models.CharField(max_length=100, blank=True)
    invite_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username