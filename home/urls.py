from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
     path('banner/create/', views.banner_create, name='banner-create'),
    path('banner/<int:id>/edit/', views.banner_edit, name='banner-edit'),
     path('banner/<int:id>/delete/' , views.banner_delete , name= 'banner-delete')
]
