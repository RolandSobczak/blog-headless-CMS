from django.urls import path, include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
routers.register('users', views.UserViewSet, "users")
routers.register('token', views.TokenViewSet, "token")

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', include(routers.urls)),
]