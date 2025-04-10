from rest_framework import viewsets, filters as rest_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Category, Product, ProductImage, FileManager
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, FileManagerSerializer
from .filters import ProductFilter

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
            queryset = queryset.annotate(
                rank=SearchRank('search_vector', query)
            ).filter(search_vector=query).order_by('-rank') 
        return queryset

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class FileManagerViewSet(viewsets.ModelViewSet):
    queryset = FileManager.objects.all()
    serializer_class = FileManagerSerializer