from functools import partial
from itertools import product
from django.contrib.auth import PermissionDenied
from django.shortcuts import render
from django.http import JsonResponse
# from requests import delete
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import ProductSerializer


# authentication classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# custom permission
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
# -------> Old way to do it
# def product_list(request):
#     """ API endpoint to get all the products"""
#     products = Product.objects.all()

#     product_data = []
#     for product in products:
#         product_data.append({
#             'id': product.id,
#             'name': product.name,
#             'description': product.description,
#             'price': str(product.price),
#             'stock': product.stock,
#             'created_at': product.created_at.isoformat(),
#         })

#     return JsonResponse({'products': product_data})


@api_view(['GET'])
def get_product(request):

    # if request.method == 'GET':
    # 1. Price Filter (min price & max price)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    product_search = request.GET.get('search')
    
    if min_price:
        products = Product.objects.filter(price__lte=min_price)

    if max_price:
        products = Product.objects.filter(price__gte=max_price)

    if product_search:
        products = Product.objects.filter(category__iexact=product_search)

    # Let's add filter 


    # Getting pagination parameters from URL
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4)) #20 is default

    # Calculation item start and end number
    start = (page -1) * page_size
    end = start + page_size

    # products = Product.objects.all()  #django model data
    products = Product.objects.all()[start : end]  #django model data
    total = Product.objects.count()


    serializer = ProductSerializer(products, many=True) #converts django object into JSON
    return Response({
        "status" : "success",
        "message" : "Products fetched successfully",
        "data" : serializer.data,
        "count" : total,
        "previous" : f'?page={page-1}' if page>1 else None,
        "next" : f'?page={page+1}' if end < total else None,
    }, status.HTTP_200_OK)



# ADDing Product
@api_view(['POST'])
# No need for @permission_classes([IsAuthenticated]) anymore!
# The global DEFAULT_PERMISSION_CLASSES handles authentication automatically
# POST requests require authentication (from IsAuthenticatedOrReadOnly)
def product_add(request):
    # Adding new Product
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        # No need as custom create() is used 
        # serializer.save(created_by=request.user)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({
        "status" : "error",
        "message" : "Invalid data provided",
        "errors" : serializer.errors,
        "received_data" : request.data
    }, status = status.HTTP_400_BAD_REQUEST)



# UPdating and Deleting Product
@api_view([ 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsOwnerOrReadOnly])  # Keep this because it's MORE SPECIFIC than the global default
# This overrides the global permission to add ownership check
def product_detail(request, pk):
    # Updating whole Product
    product = Product.objects.get(pk=pk)

    permission = IsOwnerOrReadOnly()
    if not permission.has_object_permission(request, None, product):
        raise PermissionDenied("You dont have permission to modify this product")

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : "success",
                "message" : "Product Updated succesfully",
                "data" : serializer.data
            }, status.HTTP_200_OK)
        else:
            return Response({
                "status" : "failed",
                "message" : "Data not updated Succesfully"
            }, status.HTTP_400_BAD_REQUEST)

    # Updating Few Fields
    if request.method == 'PATCH':
        serializer = ProductSerializer(product, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : "success",
                "message" : "Data Updated",
                "data" : serializer.data,
            }, status.HTTP_200_OK)

        else:
            return Response({
                "status" : "Fail",
                "message" : "Failed at saving data",
            }, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Deleting Product 
    if request.method == 'DELETE':
        product.delete()
        return Response({
            "status" : "Success",
            "message" : "Product Deleted Successfully"

        }, status.HTTP_200_OK)











