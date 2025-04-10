from rest_framework import serializers
from .models import CustomUser, TwoFactorCode, PasswordResetToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import random
import string

# This serializer is used for user registration : 
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'email', 'mobile_number', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'url': {'view_name': 'customuser-detail', 'lookup_field': 'pk'}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# This serializer is used for user login :
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            code = ''.join(random.choices(string.digits, k=6))
            TwoFactorCode.objects.create(user=user, code=code)
            try:
                send_mail(
                    subject='کد تأیید دو مرحله‌ای',
                    message=f'سلام {user.first_name}،\n\nکد تأیید شما: {code}\nاین کد تا 10 دقیقه معتبر است.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                raise serializers.ValidationError(f"خطا در ارسال ایمیل: {str(e)}")
            return user
        raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است")

# This serializer is used for verifying the two-factor authentication code :
class TwoFactorCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        code = data.get('code')
        user_id = self.context['request'].session.get('pending_user_id')
        if not user_id:
            raise serializers.ValidationError("جلسه ورود نامعتبر است")
        
        try:
            user = CustomUser.objects.get(id=user_id)
            two_factor_code = TwoFactorCode.objects.filter(user=user, code=code).latest('created_at')
            if not two_factor_code.is_valid():
                raise serializers.ValidationError("کد منقضی شده است")
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد")
        except TwoFactorCode.DoesNotExist:
            raise serializers.ValidationError("کد نامعتبر است")

# This serializer is used for updating user profile :
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'mobile_number', 
                  'birth_date', 'national_code', 'profile_picture', 'job', 'invite_code', 'wallet_balance']
        extra_kwargs = {
            'url': {'view_name': 'customuser-detail', 'lookup_field': 'pk'}
        }

# This serializer is used for password reset request :
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            return data
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("کاربری با این ایمیل یافت نشد")

# This serializer is used for password reset :
class PasswordResetSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            token = PasswordResetToken.objects.get(token=data['token'])
            if not token.is_valid():
                raise serializers.ValidationError("توکن منقضی شده است")
            return data
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("توکن نامعتبر است")