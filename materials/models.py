from django.db import models

from materials.services import NULLABLE
from user.models import User


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=100, verbose_name="Название курса")
    image = models.ImageField(
        upload_to="course/images/", verbose_name="Превью", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="course", **NULLABLE
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lesson"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    image = models.ImageField(
        upload_to="lesson/images/", verbose_name="Превью урока", **NULLABLE
    )
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="lesson", **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    """Модель способа оплаты"""

    name = models.CharField(max_length=100, verbose_name="Название способа оплаты")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Модель оплаты"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        related_name="payment",
        **NULLABLE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="payment",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Урок",
        related_name="payment",
        **NULLABLE,
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    pay_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    pay_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        verbose_name="Способ оплаты",
        related_name="payment",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата {self.amount} руб. от {self.pay_date} за {self.course if self.course else self.lesson} пользователем:{self.user.email}"


class Subscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"Подписка на курс {self.course} пользователем: {self.user.email}"
