from rest_framework import serializers

from materials.models import Course, Lesson, Payment, Subscription
from materials.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = [
            "id",
            "name",
            "description",
            "course",
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)

    def get_lessons_count(self, object):
        return object.lesson.count()

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons_count", "lesson"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    def get_is_active(self, object):
        if self.request.user == object.user:
            return True

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "course",
            "is_active"
        ]
