from django.db import models
from django.contrib.auth.models import User
from .validators import validate_image_file, validate_no_scripts

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, validators=[validate_no_scripts])
    description = models.TextField(validators=[validate_no_scripts])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['price'], name='product_price_idx'),
            models.Index(fields=['stock'], name='product_stock_idx'),
            models.Index(fields=['-created_at'], name='product_created_idx'),
            models.Index(fields=['price', 'stock'], name='product_price_stock_idx'),
        ]
        ordering = ['-created_at']  # Default ordering

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Model to store multiple images for a single product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', validators=[validate_image_file])
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_primary', '-uploaded_at']
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
    
    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


      