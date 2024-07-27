from django.db import models

from django.contrib.auth.models import AbstractUser

from materials.services import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(
        upload_to="user/avatar", verbose_name="Аватар", **NULLABLE
    )
    phone_number = models.CharField(max_length=30, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
