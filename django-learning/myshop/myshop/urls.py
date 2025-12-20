"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products import urls
from django.conf import settings
from django.conf.urls.static import static
# API Documentation imports (Topic 22)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('auth/', include('authentication.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'), #Returns raw OpenAPI schema (JSON format)
    path('docs/',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), #Swagger UI - Interactive API documentation http://127.0.0.1:8000/api/docs/
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), #ReDoc - Clean, professional documentation http://127.0.0.1:8000/api/redoc/


]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add Django Debug Toolbar URLs
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
