from rest_framework import serializers

from materials.models import Course, Lesson


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

    def get_lessons_count(self, object):
        return object.lesson.count()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons_count"
        ]


