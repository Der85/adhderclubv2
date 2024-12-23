from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Home page
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
]
