from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователей — отвечает за создание user и superuser"""

    def create_user(self, email, password=None, **extra_fields):
        # Обязательное поле — email
        if not email:
            raise ValueError("У пользователя должен быть email")
        email = self.normalize_email(email)  # Приводим email к нормальной форме
        user = self.model(email=email, **extra_fields)  # Создаём пользователя
        user.set_password(password)  # Хешируем пароль
        user.save()  # Сохраняем пользователя в базу данных
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Устанавливаем флаги суперпользователя
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Обязательно нужен пароль
        if not password:
            raise ValueError("У суперпользователя должен быть пароль")
        return self.create_user(email, password, **extra_fields)


# Кастомная модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Основной параметр — email
    is_active = models.BooleanField(default=True)  # Можно ли входить в аккаунт
    is_staff = models.BooleanField(default=False)  # Доступ в админку (для админов)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"  # Авторизация по email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email