from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from userapp.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель для создания пользователей"""

    email = models.EmailField(max_length=64, unique=True, blank=False, verbose_name='Email')

    is_staff = models.BooleanField(default=False,
                                   help_text='Определяет разрешение пользователя на вход в административную часть.',
                                   verbose_name='Moderator')

    is_active = models.BooleanField(default=True,
                                    help_text='Определяет активен ли пользователь в системе.',
                                    verbose_name='Active')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.email}"
