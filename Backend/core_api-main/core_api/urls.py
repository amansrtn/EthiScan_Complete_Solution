"""core_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from django.views.generic import RedirectView
from .admin import admin_statistics_view  # new

urlpatterns = [
    path(
        "admin/statistics/",
        admin.site.admin_view(admin_statistics_view),
        name="admin-statistics"
    ),
    path("Ethibot/",include('ethibot.urls')),
    path("chart/", include('core.urls')),
    path('imgtxtanalyzer/', include('image_feed_analyzer.urls')),
    path('admin/', admin.site.urls),
    path('logout/', RedirectView.as_view(url='/admin/logout/')),
    path('txtanalyzer/', include('text_analyzer.urls')),
    path('pureimganalyzer/', include('pure_image_analyzer.urls')),
    path('subtricky/', include('substricky.urls')),
    path('tncanalyzer/', include('tcanalyzer.urls')),
    path('', views.default),
]
