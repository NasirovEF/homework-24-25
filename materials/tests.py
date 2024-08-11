from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from materials.models import Course, Lesson, Subscription
from user.models import User
from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test05@test.ru")
        self.course = Course.objects.create(name="Skypro", description="курс скайпро")
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Описание урока 1",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Урок 5"}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок 5")

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "Урок 2",
            "description": "Описание урока 2",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_url": "https://www.youtube.com/watch",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        resolute = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "course": self.course.pk,
                    "video_url": None,
                    "image": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), resolute)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test05@test.ru")
        self.course = Course.objects.create(name="Skypro", description="курс скайпро")
        self.client.force_authenticate(user=self.user)

    def test_post_activated_sub(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get(user=self.user).user.email, self.user.email)

    def test_post_deactivated_sub(self):
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_anonym_user(self):
        self.client.logout()
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_course(self):
        url = reverse("materials:subscription")
        data = {"course_id": 2}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
