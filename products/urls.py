from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, ProductViewSet, ProductImageViewSet, 
                   FileManagerViewSet, CartViewSet, OrderViewSet, OrderItemViewSet, ReviewViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'files', FileManagerViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'reviews', ReviewViewSet, basename='review') 

urlpatterns = [
    path('', include(router.urls)),
]