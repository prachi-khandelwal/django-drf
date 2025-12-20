from django.urls import path
from . import views

# JWT imports commented out - will add when we install the package
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

urlpatterns = [

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),


    # JWT Authentication - will add later
    # path('jwt/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    # path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    # path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

]