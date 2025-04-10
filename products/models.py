from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    brand = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True, blank=True)  # فیلد برای ذخیره بردار جستجو

    def __str__(self):
        return self.name

# سیگنال برای آپدیت خودکار search_vector
@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    Product.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('name', weight='A') +
                     SearchVector('short_description', weight='B') +
                     SearchVector('long_description', weight='C')
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

class FileManager(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name