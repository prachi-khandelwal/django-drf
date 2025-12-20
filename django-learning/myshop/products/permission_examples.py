"""
GLOBAL PERMISSION STRATEGY - OVERRIDE PATTERNS
Topic 21 - Day 26

This file demonstrates different permission override patterns with examples.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

# =============================================================================
# GLOBAL DEFAULT (in settings.py):
# 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly']
# 
# This means:
# - GET requests: Anyone can access (even anonymous users)
# - POST/PUT/PATCH/DELETE: Must be authenticated
# =============================================================================


# =============================================================================
# PATTERN 1: Using Global Default (No Override)
# =============================================================================
@api_view(['GET'])
def public_endpoint(request):
    """
    This endpoint uses the GLOBAL default permission.
    
    No @permission_classes decorator = uses DEFAULT_PERMISSION_CLASSES
    
    Result:
    - GET is public (anyone can access) ✅
    """
    return Response({"message": "This is public!"})


@api_view(['POST'])
def protected_endpoint(request):
    """
    This endpoint also uses the GLOBAL default permission.
    
    No @permission_classes decorator = uses DEFAULT_PERMISSION_CLASSES
    
    Result:
    - POST requires authentication (IsAuthenticatedOrReadOnly blocks POST for anonymous) 🔒
    """
    return Response({"message": "You are authenticated!"})


# =============================================================================
# PATTERN 2: Override to MORE RESTRICTIVE
# =============================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_only_read(request):
    """
    Override the global default to make GET also require authentication.
    
    Global: IsAuthenticatedOrReadOnly (GET is public)
    Override: IsAuthenticated (GET requires authentication)
    
    Result:
    - GET requires authentication 🔒 (more restrictive than global)
    """
    return Response({"message": "You must be authenticated to see this!"})


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_only_endpoint(request):
    """
    Override the global default to require ADMIN privileges.
    
    Global: IsAuthenticatedOrReadOnly
    Override: IsAdminUser (must be staff/admin)
    
    Result:
    - Both GET and POST require admin privileges 🔒🔒
    """
    return Response({"message": "Admin only!"})


# =============================================================================
# PATTERN 3: Override to LESS RESTRICTIVE
# =============================================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def public_registration(request):
    """
    Override the global default to make POST public.
    
    Global: IsAuthenticatedOrReadOnly (POST requires auth)
    Override: AllowAny (POST is public)
    
    Result:
    - POST is public ✅ (less restrictive than global)
    
    Use case: User registration, public contact forms, etc.
    """
    return Response({"message": "Registration successful!"})


# =============================================================================
# PATTERN 4: ViewSet with Override
# =============================================================================
class PublicProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet that overrides global permission to allow ANYONE to create products.
    
    Global: IsAuthenticatedOrReadOnly (write requires auth)
    Override: AllowAny (everything is public)
    
    ⚠️ NOT RECOMMENDED in real applications! Just for demonstration.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Override global


class StrictProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet that overrides global permission to require authentication for EVERYTHING.
    
    Global: IsAuthenticatedOrReadOnly (read is public)
    Override: IsAuthenticated (both read and write require auth)
    
    Use case: Private APIs, internal tools, etc.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Override global


# =============================================================================
# SUMMARY OF PATTERNS
# =============================================================================

"""
┌─────────────────────────────────────────────────────────────────────┐
│                    PERMISSION PRIORITY ORDER                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. View-Level Override (@permission_classes or ViewSet)           │
│     ↓ Takes priority over everything                               │
│                                                                     │
│  2. Global Default (DEFAULT_PERMISSION_CLASSES in settings.py)     │
│     ↓ Used when no view-level override                             │
│                                                                     │
│  3. DRF Default (AllowAny)                                         │
│     ↓ Only if neither 1 nor 2 is set                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

WHEN TO OVERRIDE:
✅ User registration endpoint (POST should be public) → AllowAny
✅ Admin-only endpoints → IsAdminUser
✅ Custom permission logic → Custom permission class
✅ Different permission for specific endpoints

WHEN NOT TO OVERRIDE:
❌ If global default already works for your endpoint
❌ Don't repeat the same permission everywhere (defeats the purpose!)
❌ Don't use AllowAny everywhere (security risk!)

BEST PRACTICES:
1. Set a SECURE global default (IsAuthenticatedOrReadOnly or IsAuthenticated)
2. Only override when you need DIFFERENT behavior
3. Document WHY you're overriding (add comments)
4. Test both authenticated and anonymous access
"""

