from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('products/')),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ ADD THIS
]
