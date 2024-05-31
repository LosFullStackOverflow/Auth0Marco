from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('social_django.urls')),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('metaData/', views.metaData, name='metaData'),
    path('button-action/', views.metaData, name='button_action'),

]
