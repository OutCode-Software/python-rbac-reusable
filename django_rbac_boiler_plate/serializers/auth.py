
from rest_framework import serializers, exceptions
from django_rbac_boiler_plate.models import Role, RolePermission, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify


class LoginTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        return super().validate(attrs)


class RefreshTokenSerializer(TokenRefreshSerializer):
    def save(self):
        refresh = self.context['request'].data.get('refresh', '')
        RefreshToken(refresh).blacklist()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','name','slug']
        read_only_fields = ('id','slug',)

    def create(self, validated_data):
        name = validated_data.get('name')
        slug = slugify('_'.join([name]), allow_unicode=False)
        permission = Permission.objects.create(name=name, slug=slug)
        return permission

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=PermissionSerializer(),
        read_only=True
    )

    class Meta:
        model = Role
        fields = '__all__'

class RoleBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class RolesPermissionsSerializer(serializers.Serializer):
    roles = RoleSerializer(many=True)
    permissions = PermissionSerializer(many=True)


class RolePermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField()

    class Meta:
        model = RolePermission
        fields = ('role', 'permission', 'permissions',)
        extra_kwargs = {
            'permission': {'read_only': True},
        }

    # def validate(self, attrs, ):
    #     try:
    #         permissions = attrs['permissions']
    #         for permission in permissions:
    #             roles_p = RolePermission.objects.filter(role_id=attrs['role']).values_list('permission', flat=True)
    #             if permission in roles_p:
    #                 raise serializers.ValidationError("This permission is already set for this role.")
    #     except RolePermission.DoesNotExist:
    #         pass  # skip
    #     return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['role'] = RolePermission(instance.role)
        data['role'] = instance.role.name
        return data

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        role = validated_data.get('role')
        for permission in permissions:
            role_permission = RolePermission.objects.create(permission_id=permission, role=role)
        return role_permission

    def update(self, instance, validated_data):
        print(validated_data['role'])



class RolesPermissionListSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer()
    class Meta:
        model = RolePermission
        fields = ['permission']