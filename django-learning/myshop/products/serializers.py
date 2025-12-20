from rest_framework import serializers
from .models import Product, ProductImage
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model - handles multiple images per product"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'order', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_image_url(self, obj):
        """Return full URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_available = serializers.SerializerMethodField()
    total_inv_val = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_price(self, value):
        """Validate that price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        """Validate that stock cannot be negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
    
    def get_is_available(self, obj):
        """Calculate if product is available (has stock)"""
        return obj.stock > 0

    def get_total_inv_val(self, obj):
        """ Calculates Total inventory value"""
        return obj.stock * obj.price
    
    def get_formatted_price(self, obj):
        """Format price with currency symbol and thousands separator"""
        return f"${obj.price:,.2f}"
    
    def get_image_url(self, obj):
        """Return full URL for the image if it exists"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def create(self, validated_data):
        """Custom create method to set created_by from request"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Custom update method to handle product updates"""
        # Update all fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save the updated instance
        instance.save()
        return instance
    
    def validate(self, data):
        """Object-level validation: validate multiple fields together"""
        price = data.get('price')
        description = data.get('description')
        stock = data.get('stock')
        name = data.get('name')
        
        # Rule 1: Expensive products need detailed descriptions
        if price and price > 10000:
            if not description or len(description) < 50:
                raise serializers.ValidationError(
                    "Expensive products (>$10,000) must have a detailed description (at least 50 characters)."
                )
        
        # Rule 2: Products with zero stock should indicate it in the name
        if stock is not None and stock == 0:
            if name and 'out of stock' not in name.lower():
                raise serializers.ValidationError(
                    "Products with zero stock must include 'Out of Stock' in the name."
                )
        
        # Rule 3: Cheap products can't have excessive stock (prevents hoarding)
        if price and price < 10 and stock and stock >= 100:
            raise serializers.ValidationError(
                "Cheap products (<$10) cannot have stock of 100 or more. Consider increasing the price or reducing stock."
            )
        
        return data