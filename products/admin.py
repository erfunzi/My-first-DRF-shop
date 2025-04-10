from django.contrib import admin
from .models import Category, Product, ProductImage, FileManager, Cart, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'brand')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')

@admin.register(FileManager)
class FileManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'is_active')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    list_editable = ('is_approved',)
    search_fields = ('user__username', 'product__name', 'comment')