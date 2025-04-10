from django_filters import rest_framework as filters
from .models import Product

# This filter class is used to filter products based on various criteria.
class ProductFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name='brand', lookup_expr='iexact')  
    size = filters.CharFilter(field_name='size', lookup_expr='iexact')   
    color = filters.CharFilter(field_name='color', lookup_expr='iexact')  
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte') 
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')  

    class Meta:
        model = Product
        fields = ['brand', 'size', 'color', 'min_price', 'max_price']