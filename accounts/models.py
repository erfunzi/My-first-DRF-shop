from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone

# Custom user model extending AbstractUser :
# This model can be used for user authentication and management 
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

# Two-factor authentication code model :
class TwoFactorCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='two_factor_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"Code {self.code} for {self.user.username}"

# Password reset token model : 
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)  
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"Reset token for {self.user.username}"