from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# سریالایزر برای ثبت‌نام
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

# سریالایزر برای ورود
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است")

# سریالایزر برای پروفایل
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'mobile_number', 
                  'birth_date', 'national_code', 'profile_picture', 'job', 'invite_code', 'wallet_balance']
        extra_kwargs = {
            'url': {'view_name': 'customuser-detail', 'lookup_field': 'pk'}
        }