from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django_rbac_boiler_plate.serializers import PermissionSerializer, RoleBasicSerializer
from django_rbac_boiler_plate.models import Permission, Role


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAdminUser,)
    serializer_class = PermissionSerializer


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAdminUser,)
    serializer_class = RoleBasicSerializer