from django.contrib import admin
from django.urls import path , include
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('post/<str:slug>', views.blog_post, name='blog-post'),
    path('search', views.search_blogs, name='blog-search'),
    path('create/', views.blog_create, name='blog-create'),
    path('blogs/<int:id>/edit/', views.blog_edit, name='blog-edit'),
    path('blogs/<int:id>/delete/', views.blog_delete, name='blog-delete'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/<int:id>/edit/', views.category_edit, name='category-edit'),
    path('categories/<int:id>/delete/', views.category_delete, name='category-delete'),
    path('subcategories/create/', views.subcategory_create, name='subcategory-create'),
    path('subcategories/<int:id>/edit/', views.subcategory_edit , name ='subcategories-edit'),
    path('subcategory/<int:id>/delete/' , views.subcategory_delete , name= 'subcategories-delete')



]
