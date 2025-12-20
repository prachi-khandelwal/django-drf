from django.contrib import admin
from .models import Product, ProductImage


# Inline admin for ProductImage - allows managing images within Product admin page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary', 'order')
    readonly_fields = ('uploaded_at',)


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    list_filter = ('created_at', 'updated_at')
    list_editable = ['price', 'stock']
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    list_per_page = 10
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'order', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('product__name',)
    ordering = ('product', 'order')