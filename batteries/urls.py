from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'batteries'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='batteries/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my/', views.my_submissions, name='my_submissions'),
]
