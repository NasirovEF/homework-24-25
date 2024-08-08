from django.core.management import BaseCommand
from user.models import User
import os
from dotenv import load_dotenv
from config.settings import BASE_DIR

dot_env = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dot_env)


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv("CSU_EMAIL"),
            is_superuser=True,
            is_staff=True,
            phone_number=os.getenv("CSU_PHONE_NUMBER"),
            city="Volgograd",
        )

        user.set_password(os.getenv("CSU_PASSWORD"))
        user.save()
