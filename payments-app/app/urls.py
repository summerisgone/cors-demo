"""wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from rest_framework import routers
from wallet import api

router = routers.DefaultRouter()
router.register(r'wallet', api.WalletViewSet, base_name='wallet')
router.register(r'transfer', api.TransferViewSet, base_name='transfer')

urlpatterns = [
    path('', include('wallet.urls')),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
