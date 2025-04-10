from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from accounts.models import CustomUser


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
    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return self.name

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

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.user.username}"

    class Meta:
        unique_together = ('user', 'product')

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('processed', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"

    class Meta:
        unique_together = ('user', 'product') 