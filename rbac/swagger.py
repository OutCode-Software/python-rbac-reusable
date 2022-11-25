"""
v1 view for swagger
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


swagger_info = openapi.Info(
   title="RBAC",
   default_version='v1',
   description="APIs of RABC",
   contact=openapi.Contact(email="suresh.shrestha@outcodesoftware.com"),
   license=openapi.License(name="BSD License"),
)


drf_yasg_swagger_view = get_schema_view(
   swagger_info,
   public=True,
   permission_classes=[permissions.AllowAny],
)
