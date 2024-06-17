
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.default),
    path('update/', views.updateStock)
]