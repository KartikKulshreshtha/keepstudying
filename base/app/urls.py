from django.urls import path
from . import views

urlpatterns = [
    path('loginPage/', views.loginPage, name='loginPage'),
    path('logoutPage/', views.logoutPage, name='logoutPage'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    path('createroom/', views.createroom, name='create-room'),
    path('updateroom/<str:pk>/', views.updateroom, name='update-room'),
    path('deleteroom/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('deleteMessage/<str:pk>/', views.deleteMessage, name='deleteMessage'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('topics/', views.topicsPage, name='topicsPage'),
    path('activity/', views.activitiesPage, name='activitiesPage'),
]
