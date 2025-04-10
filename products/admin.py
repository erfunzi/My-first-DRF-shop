from django.contrib import admin
from .models import Category, Product, ProductImage, FileManager

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_active')
    list_filter = ('is_active', 'category', 'brand')
    search_fields = ('name', 'brand')
    list_editable = ('price', 'stock', 'is_active')
    inlines = [ProductImageInline]  

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')
    list_filter = ('is_main',)

@admin.register(FileManager)
class FileManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)