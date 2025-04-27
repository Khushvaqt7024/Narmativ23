"""
URL configuration for xah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from functools import partial

from django.contrib import admin
from django.db import router
from django.http import HttpResponse
from django.template.context_processors import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from xah import settings
# def index(request):
#     name = request.GET.get('name', "")
#     return HttpResponse(f"Hello, World! {name} ")
#
#
# urlpatterns = [
#     path('', include('profiles.urls')),
#     path('accounts/', include('accounts.urls')),
#     path("", index, name="index"),
#     path('admin/', admin.site.urls),
#     path('book/', include('book.urls')),
#     path('contact/', include('contact.urls')),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
#
# urlpatterns += static(settings.MEDIA_URL)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('accounts/', include('accounts.urls')),
    path('book/', include('book.urls')),
    path('contact/', include('contact.urls')),
    path('files/', include('files.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)