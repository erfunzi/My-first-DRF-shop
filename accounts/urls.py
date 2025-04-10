from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, UserProfileView, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('', include(router.urls)), 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]