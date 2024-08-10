from rest_framework import serializers

from materials.models import Course, Lesson, Payment, Subscription
from materials.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "course", "video_url", "image"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)
    subscribers = serializers.SerializerMethodField()

    def get_lessons_count(self, object):
        return object.lesson.count()

    def get_subscribers(self, object):
        return [sub.user.email for sub in Subscription.objects.filter(course=object)]

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons_count", "lesson", "subscribes"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ["id", "user", "course"]
