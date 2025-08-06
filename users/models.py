from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        verbose_name="Username",
        blank=True,
        null=True,
        help_text="Введите свое имя",
    )
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузити фотографию",
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    # telegram = models.CharField(
    #     max_length=15,
    #     verbose_name="Телеграм",
    #     help_text="Введите телеграма",
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []