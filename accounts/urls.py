from django.urls import path, include
from . import views
from accounts import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
