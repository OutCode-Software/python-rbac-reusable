import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_rbac_boiler_plate.managers import UserManager

class TimestampMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True

class User(TimestampMixin, PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    username = models.CharField(max_length=254, unique=True, null=False, default="")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        ordering = ['email', 'first_name', 'last_name']
        db_table = 'core_user'

    def __str__(self):
        return "{} {}".format(self.full_name, self.email)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    @property
    def roles(self):
        try:
            return self.user_role.all()
        except ObjectDoesNotExist as _:
            return []