from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Avg, Sum, Count
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter
from .throttles import BurstRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Get a paginated list of all products with filtering and search"
    ),
    retrieve=extend_schema(
        summary="Get product details",
        description="Retrieve detailed information about a specific product by ID"
    ),
    create=extend_schema(
        summary="Create a new product",
        description="Create a new product. Requires authentication. You will be set as the owner"
    ),
     update=extend_schema(
        summary="Update a product",
        description="Full update of a product. Only the owner can update. All fields required"
    ),
    partial_update=extend_schema(
        summary="Partially update a product",
        description="Partial update of a product. Only the owner can update. Send only fields to change"
    ),
    destroy=extend_schema(
        summary="Delete a product",
        description="Delete a product. Only the owner can delete. This action cannot be undone"
    )
)
@method_decorator(cache_page(60), name='list')  # Cache the list view for 60 seconds
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    
    This ViewSet provides CRUD operations for products:
    - **list**: Get all products (with pagination, filtering, search)
    - **create**: Create a new product (requires authentication)
    - **retrieve**: Get a single product by ID
    - **update**: Update a product (owner only)
    - **partial_update**: Partially update a product (owner only)
    - **destroy**: Delete a product (owner only)
    
    **Filtering:**
    - `?price_min=10&price_max=100` - Filter by price range
    - `?in_stock=true` - Show only in-stock products
    - `?search=laptop` - Search in name/description
    - `?ordering=-price` - Sort by price (descending)
    
    **Authentication:**
    - GET requests: Public (no authentication needed)
    - POST/PUT/PATCH/DELETE: Requires authentication
    - Update/Delete: Only product owner can modify
    """
    # not optimised (N+1) DB calls
    # queryset = Product.objects.all().order_by('-created_at')

    queryset = Product.objects.select_related('created_by').prefetch_related('images').all().order_by('-created_at')
    serializer_class = ProductSerializer
    # Removed IsAuthenticatedOrReadOnly because it's now the GLOBAL default
    # We only specify IsOwnerOrReadOnly which is MORE SPECIFIC than the default
    permission_classes = [IsOwnerOrReadOnly]
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Use custom filter class for advanced filtering
    filterset_class = ProductFilter
    
    # Specify which fields can be searched (text search)
    # ^ = starts with, no prefix = contains
    search_fields = ['^name', 'description']
    
    # Specify which fields can be used for ordering/sorting
    ordering_fields = ['price', 'stock', 'created_at']
    
    def get_throttles(self):
        """
        Override throttles based on the action.
        - 'create' action uses stricter BurstRateThrottle (3/min)
        - All other actions use default throttling (5/min anon, 100/min user)
        """
        if self.action == 'create':
            # Apply stricter throttle for creating products
            return [BurstRateThrottle()]
        # Use default throttles for all other actions
        return super().get_throttles()
    
    def list(self, request, *args, **kwargs):
        """
        Override the list method to add MANUAL caching.
        This demonstrates how manual caching works for product list.
        
        THE FLOW:
        
        FIRST REQUEST: GET /products/
        1. cache.get('product_list') → Returns None (empty)
        2. Query database: Product.objects.all() → [P1, P2, P3]
        3. cache.set('product_list', [P1, P2, P3]) → Store in cache
        4. Return [P1, P2, P3] to user
        
        SECOND REQUEST: GET /products/ (within 5 min)
        1. cache.get('product_list') → Returns [P1, P2, P3] (found!)
        2. Return cached list immediately (NO database query!)
        
        WHEN NEW PRODUCT CREATED:
        1. perform_create() runs → cache.delete('product_list')
        2. Cache is now empty
        
        NEXT REQUEST AFTER CREATION: GET /products/
        1. cache.get('product_list') → Returns None (was deleted!)
        2. Query database: Product.objects.all() → [P1, P2, P3, P4] (NEW!)
        3. cache.set('product_list', [P1, P2, P3, P4]) → Store fresh data
        4. Return [P1, P2, P3, P4] to user ✅ UPDATED!
        """
        
        # STEP 1: Define cache key
        cache_key = 'product_list'
        
        # STEP 2: Try to get from cache first
        cached_products = cache.get(cache_key)
        
        # STEP 3: If found in cache, return it (FAST!)
        if cached_products is not None:
            print("✅ CACHE HIT! Returning cached product list")
            # Return the cached response
            return Response({
                'cached': True,
                'message': 'This list came from cache! ⚡',
                'results': cached_products
            })
        
        # STEP 4: Cache MISS - Get from database (SLOW)
        print("❌ CACHE MISS! Querying database for products")
        response = super().list(request, *args, **kwargs)
        
        # STEP 5: Store the response data in cache for 5 minutes
        cache.set(cache_key, response.data, timeout=300)
        print("💾 Saved to cache for 5 minutes")
        
        # STEP 6: Add metadata to show it's fresh data
        response.data['cached'] = False
        response.data['message'] = 'Fresh from database! 🐌'
        
        return response
    
    def perform_create(self, serializer):
        """
        Called when creating a new product.
        DELETE the cached product list so next request gets fresh data!
        """
        super().perform_create(serializer)
        
        # Delete the cached product list
        cache.delete('product_list')
        print("🗑️ Deleted cached product list (so next request gets fresh data)")
        
        # Also delete statistics cache
        
        cache.delete('product_statistics')
        
    def perform_update(self, serializer):
        """
        Called when updating a product.
        DELETE the cached product list (price/name might have changed!)
        """
        super().perform_update(serializer)
        cache.delete('product_list')
        cache.delete('product_statistics')
        print("🗑️ Deleted cached product list (product was updated)")
        
    def perform_destroy(self, instance):
        """
        Called when deleting a product.
        DELETE the cached product list (product no longer exists!)
        """
        super().perform_destroy(instance)
        cache.delete('product_list')
        cache.delete('product_statistics')
        print("🗑️ Deleted cached product list (product was deleted)")
    

    @extend_schema(
    summary="Product Statistics",
    description="Get aggregate statistics about all products",
     responses={
        200: {
            'type': 'object',
            'properties': {
                'total_products': {'type': 'integer', 'example': 42},
                'average_price': {'type': 'number', 'example': 299.99},
                'total_inventory_value': {'type': 'number', 'example': 12599.58},
                'out_of_stock_count': {'type': 'integer', 'example': 3},
            }
        }
    }, 
    tags=['Statistics'])
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Custom endpoint: GET /products/statistics/
        
        MANUAL CACHING FLOW (Read this carefully!):
        
        FIRST TIME:
        1. User requests statistics → cache.get() returns None (not cached yet)
        2. We calculate stats from database (slow: 100ms)
        3. We save stats to cache → cache.set('product_statistics', stats)
        4. Return stats to user
        
        SECOND TIME (within 5 minutes):
        1. User requests statistics → cache.get() returns stats (found in cache!)
        2. Return cached stats immediately (fast: 5ms) - NO database query!
        
        WHEN PRODUCT IS CREATED:
        1. perform_create() runs → cache.delete('product_statistics')
        2. Cache is now empty (deleted)
        
        NEXT REQUEST AFTER CREATION:
        1. User requests statistics → cache.get() returns None (cache was deleted!)
        2. We calculate FRESH stats (with the new product included!)
        3. We save NEW stats to cache
        4. Return FRESH stats to user
        
        This is how we keep cache up-to-date!
        """
        
        # STEP 1: Try to get from cache (like checking if you have leftovers in fridge)
        cache_key = 'product_statistics'
        cached_stats = cache.get(cache_key)
        
        # STEP 2: If found in cache, return it immediately (fast!)
        if cached_stats is not None:
            cached_stats['cached'] = True
            cached_stats['message'] = 'From cache! ⚡'
            return Response(cached_stats)
        
        # STEP 3: Not in cache, so calculate it (slow, but necessary)
        stats = {
            'total_products': Product.objects.count(),
            'average_price': Product.objects.aggregate(Avg('price'))['price__avg'],
            'total_stock': Product.objects.aggregate(Sum('stock'))['stock__sum'],
            'cached': False,
            'message': 'Calculated fresh! 🐌'
        }
        
        # STEP 4: Save to cache for next time (expires in 5 minutes)
        cache.set(cache_key, stats, timeout=300)
        
        # STEP 5: Return the stats
        return Response(stats)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def upload_image(self, request, pk=None):
        """
        Custom action to upload an image for a specific product.
        URL: POST /products/{id}/upload_image/
        
        Request body should include:
        - image: The image file
        - is_primary: Boolean (optional, default False)
        - order: Integer (optional, default 0)
        """
        product = self.get_object()
        
        # Create ProductImage instance
        serializer = ProductImageSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response({
                'message': 'Image uploaded successfully',
                'image': serializer.data
            }, status=201)
        
        return Response(serializer.errors, status=400)