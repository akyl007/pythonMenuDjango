from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.menu_test_view, name='menu_test'),
    path('home/',views.home,name='home'),
]
