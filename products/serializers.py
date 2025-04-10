from rest_framework import serializers
from .models import Category, Product, ProductImage, FileManager, Cart, Order, OrderItem, Review


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='category-detail')

    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'parent', 'children', 'image', 'is_active']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'product', 'image', 'is_main']

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='customuser-detail', read_only=True)
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'url', 'user', 'product', 'product_id', 'rating', 'comment', 'created_at', 'updated_at', 'is_approved']
        extra_kwargs = {
            'url': {'view_name': 'review-detail', 'lookup_field': 'pk'}
        }

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', queryset=Category.objects.all())
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'price', 'stock', 'discount', 'brand', 'size', 'color', 
                  'is_active', 'short_description', 'long_description', 'category', 'main_image', 'images', 'reviews']

class FileManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileManager
        fields = ['id', 'url', 'name', 'file', 'uploaded_at', 'is_active']

class CartSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'url', 'user', 'product', 'product_id', 'quantity', 'created_at']
        extra_kwargs = {
            'url': {'view_name': 'cart-detail', 'lookup_field': 'pk'}
        }

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'url', 'order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='customuser-detail', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'user', 'created_at', 'updated_at', 'total_price', 'status', 'shipping_address', 'items']
        extra_kwargs = {
            'url': {'view_name': 'order-detail', 'lookup_field': 'pk'}
        }