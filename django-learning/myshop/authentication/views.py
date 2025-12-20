
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# authentication classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# Create your views here.
@api_view(['POST'])
def register_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:  # ✅ Validate input exists
        return Response({
            'status': 'error',
            'message': 'Username and password required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username = username).exists():
        return Response({
            'status' : 'error',
            'message' : 'User already exists',
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        User.objects.create_user(username=username, password=password)
        return Response({
            'status':'success',
            'message' : 'User Created Successfully',

        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")


    if not username or not password:  # ✅ Validate input
        return Response({
            'status': 'error',
            'message': 'Username and password required'
        }, status=status.HTTP_400_BAD_REQUEST)


    user = authenticate(username = username , password = password)
    if user is None:
        return Response({
            'status' : "error",
            "message" : "erorr user not found",
        }, status.HTTP_401_UNAUTHORIZED)
    else:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key,
            'status' : "success",
            'message' : "user verfied"
        }, status.HTTP_200_OK)
         

