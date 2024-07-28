from rest_framework import serializers

from materials.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
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
