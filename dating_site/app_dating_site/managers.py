from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """Менеджер пользователя.
    """

    def create_user(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Пароль должен быть установлен')
        if not email:
            raise ValueError('У пользователя должен быть email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email), password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
