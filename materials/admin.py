from django.contrib import admin

from materials.models import Course, Lesson, PaymentMethod, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "course", "video_url", "image")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ("id", "user", "course", "lesson", "amount", "pay_date", "pay_method")
