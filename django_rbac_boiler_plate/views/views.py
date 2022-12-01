from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework import status,mixins,permissions
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_401_UNAUTHORIZED

from django_rbac_boiler_plate.models import Role, RolePermission, User, Permission
from django_rbac_boiler_plate.permissons import JSON_PERMISSIONS
from django_rbac_boiler_plate.serializers import RolesPermissionsSerializer, \
    RolePermissionSerializer, RolesPermissionListSerializer, LoginTokenSerializer, RefreshTokenSerializer, \
    PermissionSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from django_rbac_boiler_plate.utils import on_state_change_push_notification


class LoginViewSet(TokenObtainPairView):
    serializer_class = LoginTokenSerializer
    def post(self, request, *args, **kwargs):
        if not User.objects.filter(username=request.data['username'], is_active=True).exists():
            return Response({'message': "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            response = super().post(request, *args, **kwargs)
            user = User.objects.filter(username=request.data['username']).first()
            data = {
                'access': response.data['access'],
                'refresh': response.data['refresh'],
                'name' : user.first_name + ' ' + user.last_name,
            }
            #Test Puropose for push Notification

            # title = 'Push Notification'
            # body = 'Test Push notification send to User'
            # on_state_change_push_notification(request.user, title, body)
            return Response({'data':data, 'message':'success'}, status=status.HTTP_200_OK)

        except Exception:
            return Response({'message': 'No active account found with the given credentials.'},
                            status=HTTP_401_UNAUTHORIZED)

class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError:
            pass
        return Response({'detail': 'Successfully logged out.'})

class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class RolesPermissionsView(ListAPIView):
    serializer_class = RolesPermissionsSerializer
    queryset = None
    permission_classes = (IsAdminUser,)

    class DataModel:
        roles = Role.objects.all()
        permissions = Permission.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.DataModel)
        return Response(serializer.data)


class RolesPermissionsReteriveView(RetrieveAPIView):
    serializer_class = RolesPermissionsSerializer
    queryset = None
    # permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        role = Role.objects.filter(id=id).values().first()
        permission = RolePermission.objects.filter(role_id=role['id']).values_list('permission', flat=True)
        print(permission)
        data = {
            'id': role['id'],
            'name': role['name'],
            'permission': permission
        }
        return Response({'data': data, 'message': 'success'})


class RolePermissionView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = RolePermissionSerializer
    queryset = RolePermission.objects.all()
    # permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Permission added successfully for selected role.'
            }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        permissions = request.data.get('permissions')
        role = request.data.get('role')
        rolePermission = RolePermission.objects.filter(role_id=role)
        if rolePermission:
            rolePermission.delete()
        if not permissions:
            return Response(
                {
                    'message': 'Permission updated successfully for selected role.'
                }, status=status.HTTP_201_CREATED)
        for permission in permissions:
            role_permission = RolePermission.objects.create(permission_id=permission, role_id=role)

        return Response(
            {
                'message': 'Permission updated successfully for selected role.'
            }, status=status.HTTP_201_CREATED)

class GetPermissionsView(ListAPIView):
    serializer_class = RolesPermissionListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        roles = user.user_role.all().order_by('-id')
        permissions = []
        for role in roles:

            if role.permissions.exists():
                for permission in role.permissions.all():
                    permissions.append(permission)
        return permissions

