from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = [
            "name",
            "lessons",
        ]


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "name",
            "description",
            "course",
        ]
