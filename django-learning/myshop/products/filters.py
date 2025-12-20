import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Custom filter for Product model with advanced filtering options.
    Allows price ranges, stock comparisons, and date filtering.
    """
    # Price filtering with range
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'gte', 'lte'],
            'stock': ['exact', 'gte', 'lte'],
            'created_by': ['exact'],
        }

