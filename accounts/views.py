from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, PasswordResetToken, TwoFactorCode
from .serializers import (RegisterSerializer, LoginSerializer, UserProfileSerializer, 
                         TwoFactorCodeSerializer, PasswordResetRequestSerializer, PasswordResetSerializer)
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings

# register : 
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "ثبت‌نام با موفقیت انجام شد", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login : 
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            request.session['pending_user_id'] = user.id
            return Response({"message": "کد تأیید به ایمیل شما ارسال شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# email verification : 
class TwoFactorVerifyView(APIView):
    def post(self, request):
        user_id = request.session.get('pending_user_id')
        if not user_id:
            return Response({"error": "جلسه ورود نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = TwoFactorCodeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                two_factor_code = TwoFactorCode.objects.filter(user=user, code=serializer.validated_data['code']).latest('created_at')
                if not two_factor_code.is_valid():
                    return Response({"error": "کد منقضی شده است"}, status=status.HTTP_400_BAD_REQUEST)
                login(request, user)
                del request.session['pending_user_id']
                return Response({"message": "ورود با موفقیت انجام شد"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "کاربر یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)
        except TwoFactorCode.DoesNotExist:
            return Response({"error": "کد نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)

# logout : 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "خروج با موفقیت انجام شد"}, status=status.HTTP_200_OK)

# User Profile : 
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پروفایل به‌روزرسانی شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Request : 
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            token = PasswordResetToken.objects.create(user=user)
            reset_url = f"http://127.0.0.1:8000/api/accounts/password-reset-confirm/?token={token.token}"
            try:
                send_mail(
                    subject='بازیابی رمز عبور',
                    message=f'سلام {user.first_name}،\n\nبرای بازیابی رمز عبور خود، روی لینک زیر کلیک کنید:\n{reset_url}\nاین لینک تا 1 ساعت معتبر است.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return Response({"message": "لینک بازیابی به ایمیل شما ارسال شد"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"خطا در ارسال ایمیل: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Confirm :
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = PasswordResetToken.objects.get(token=serializer.validated_data['token'])
            user = token.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            token.delete()  # حذف توکن بعد از استفاده
            return Response({"message": "رمز عبور با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User List and Detail ViewSet :
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]