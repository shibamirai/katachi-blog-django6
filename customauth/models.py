from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        与えられたメールアドレス、名前、パスワードでユーザを作成する
        """
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        与えられたメールアドレス、名前、パスワードでスーパーユーザを作成する
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(verbose_name='名前', max_length=100)
    email = models.EmailField(verbose_name='メールアドレス', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @property
    def is_staff(self):
        """
        管理サイトへのアクセスを許可するかを返す。
        管理者権限があれば OK とする。
        """
        return self.is_admin
