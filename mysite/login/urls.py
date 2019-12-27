from django.contrib import admin
from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('<int:pk>/update/', views.update),
    path('<int:pk>/profile_update/', views.profile_update),
#    path('user/<int:pk>/profile/', views.profile, name='profile'),
#    path('user/<int:pk>/profile/update/', views.profile_update, name='profile_update'),
#    path('user/<int:pk>/pwdchange/', views.profile_change, name='profile_change'),
]
