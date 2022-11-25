from django.contrib import admin
from .models.user_auth import User
from .models.roles_permissions import Role
# Register your models here.
admin.site.register(User)
admin.site.register(Role)