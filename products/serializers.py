from rest_framework import serializers
from .models import Category, Product, ProductImage, FileManager

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='category-detail')

    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'parent', 'children', 'image', 'is_active']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'product', 'image', 'is_main']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', queryset=Category.objects.all())
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'price', 'stock', 'discount', 'brand', 'size', 'color', 
                  'is_active', 'short_description', 'long_description', 'category', 'main_image', 'images']

class FileManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileManager
        fields = ['id', 'url', 'name', 'file', 'uploaded_at', 'is_active']