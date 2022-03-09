from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер, который отвечает за создание user и superuser"""
    def _create_user(self, email, password, is_staff, is_superuser, is_active=False, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, is_active=False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, is_active=True, **extra_fields)
