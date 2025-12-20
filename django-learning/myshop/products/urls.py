from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import ProductViewSet


# Create a router
router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    # Old function-based views (keeping for comparison)
    # path('', views.get_product, name='products_list'),
    # path('<int:pk>/', views.product_detail, name='product_detail'),
    # path('add/', views.product_add, name='product_add')
    
    # New ViewSet with Router (uncomment to use)
    path('', include(router.urls)),
]