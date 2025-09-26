from  . import views
from django.urls import path 
app_name = 'user'   
urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
 
    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='change-password'),
    path('dashboard', views.admin_dashboard, name='dashboard'),
    path('blogs', views.all_blogs, name='all-blogs'),
]

