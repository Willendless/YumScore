from django.contrib import admin
from django.urls import path
from . import views

app_name = 'scoringsystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('<int:user_id>/user/', views.homepage, name='home'),
    path('<int:business_id>/business', views.business),
    path('<int:business_id>/review', views.review),
    path('<int:business_id>/review_post', views.review_post),
    path('<int:review_id>/vote/<int:vote_op>', views.vote),
    path('<int:business_id>/photos', views.photos),
    path('search/', views.search),
    path('search_all/', views.search_all),
]
