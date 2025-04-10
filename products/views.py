from rest_framework import viewsets, status, filters as rest_filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db import transaction
from .models import Category, Product, ProductImage, FileManager, Cart, Order, OrderItem, Review
from .serializers import (CategorySerializer, ProductSerializer, ProductImageSerializer, 
                         FileManagerSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer)
from .filters import ProductFilter
from django.db import models


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'short_description', 'long_description']

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            query = SearchQuery(search_query)
            vector = SearchVector('name', weight='A') + \
                     SearchVector('short_description', weight='B') + \
                     SearchVector('long_description', weight='C')
            queryset = queryset.annotate(
                rank=SearchRank(vector, query)
            ).filter(rank__gte=0.1).order_by('-rank')

        if not self.request.user.is_staff: 
            queryset = queryset.prefetch_related(
                models.Prefetch('reviews', queryset=Review.objects.filter(is_approved=True))
            )
        return queryset

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class FileManagerViewSet(viewsets.ModelViewSet):
    queryset = FileManager.objects.all()
    serializer_class = FileManagerSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "سبد خرید خالی است"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            for item in cart_items:
                if item.product.stock < item.quantity:
                    return Response({"error": f"موجودی {item.product.name} کافی نیست"}, 
                                  status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=request.data.get('shipping_address', '')
            )

            for item in cart_items:
                product = item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price
                )
                product.stock -= item.quantity
                product.save()

            cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Review.objects.filter(user=self.request.user)
        if self.request.user.is_staff: 
            queryset = Review.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)