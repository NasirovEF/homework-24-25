from datetime import timedelta

from config import settings
from django.core.mail import send_mail
from celery import shared_task

from user.models import User


@shared_task
def send_email(url, course, recipient):
    send_mail(
        subject=f"Обновление курса{course.name}",
        message=f"Внимание на курсе {course.name} произошли обновления. Для ознакомления пройдите по ссылке: {url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
    )


@shared_task
def user_verification():
    users = User.objects.all()
    timezone = settings.TIMEZONE

    for user in users:
        delta = timezone.now() - user.last_login
        if delta > 30:
            user.is_active = False
            user.save()
