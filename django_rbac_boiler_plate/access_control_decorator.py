from functools import wraps

from rest_framework.exceptions import PermissionDenied


def access_controller(permissions):

    def param_decorator(view):
        
        @wraps(view)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            
            user_roles = request.user.user_role.first()
            user_permissions = list({permission for permission in user_roles.role.permissions})
            if not any(permission in user_permissions for permission in permissions):
                raise PermissionDenied
            return view(self, request, *args, **kwargs)
        
        return wrapper
    return param_decorator