from rest_framework import routers
from django.urls import path

from . import views
from .views import viewsets

router = routers.DefaultRouter()

router.register(r'permissions', viewsets.PermissionViewSet, basename='permission')
router.register(r'roles', viewsets.RoleViewSet, basename='roles')

urlpatterns = [
    path('login/', views.LoginViewSet.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name="logout"),
    path('roles-and-permissions/', views.RolesPermissionsView.as_view(), name='roles-and-permission'),
    path('roles-and-permissions/<id>/', views.RolesPermissionsReteriveView.as_view(), name='roles-and-permission'),
    path('role-permission/', views.RolePermissionView.as_view(), name='role-permission'),
    path('get-my-permissions/', views.GetPermissionsView.as_view(), name='get-my-permission'),
    path('auth/refresh', views.RefreshTokenView.as_view(), name="refresh-token"),

]

urlpatterns += router.urls
