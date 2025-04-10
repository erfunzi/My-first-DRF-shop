from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterView, LoginView, LogoutView, UserProfileView, CustomUserViewSet, 
                   TwoFactorVerifyView, PasswordResetRequestView, PasswordResetConfirmView)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('two-factor-verify/', TwoFactorVerifyView.as_view(), name='two-factor-verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]