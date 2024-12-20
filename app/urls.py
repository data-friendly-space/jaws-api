"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include

from user_management.interfaces.controllers.csrf_token_controller import csrf_token_controller


def redirect_to_health(request):
    return redirect('/jaws-api/health')


urlpatterns = [
    path('', redirect_to_health),
    path('admin/', admin.site.urls),

    path('jaws-api/health', include('health_check.urls')),
    path('auth/', include('social_django.urls', namespace='social')),

    path('jaws-api/user-management/', include('user_management.user_management_urls')),

    path('jaws-api/analysis/', include('analysis.urls')),

    path('jaws-api/csrf', csrf_token_controller, name='csrf'),
]
