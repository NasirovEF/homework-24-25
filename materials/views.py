from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from materials.models import Course, Lesson, Payment, Subscription
from materials.pagination import LessonPagination, CoursePagination
from materials.permissions import IsModerPermission, IsOwnerPermission
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerPermission,)
        elif self.action in ["update", "retrieve", "partial_update()"]:
            self.permission_classes = (IsModerPermission | IsOwnerPermission,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerPermission & IsOwnerPermission,)

        return super().get_permissions()


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerPermission | IsOwnerPermission,
    )


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerPermission | IsOwnerPermission,
    )


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsOwnerPermission,)


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course", "lesson", "pay_method")
    ordering_fields = ("-pay_date",)


class SubscriptionAPIView(APIView):
    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )
        print(subscription)
        if not created:
            subscription.delete()
            message = "Subscription removed"
        else:
            message = "Subscription added"

        return Response({"message": message}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
