from django.contrib.auth.models import UserManager


class UserManager(UserManager):

    def create_user(self, password=None, save=True, **extra_fields):
        # email = UserManager.normalize_email(email)
        user = self.model(
            # email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            **extra_fields)
        user.set_password(password)
        if save:
            user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        user = self.create_user(password, save=False, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
