from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile/', views.profilePage, name='profile'),
    path('edit_profile/', views.editProfile, name='edit_profile'),
]