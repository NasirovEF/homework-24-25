from django.db import models

from materials.services import NULLABLE


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=100, verbose_name="Название курса")
    image = models.ImageField(
        upload_to="course/images/", verbose_name="Превью", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание курса")

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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
