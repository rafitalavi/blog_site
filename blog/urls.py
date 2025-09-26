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
]
