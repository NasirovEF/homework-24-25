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

from materials.services import get_product, get_price, get_session
from materials.tasks import send_email


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        host = self.request.get_host()
        url = f"https//{host}/materials/course/{self.serializer.pk}"
        recipient_list = serializer.subscriptions.user
        for recipient in recipient_list:
            send_email.delay(url, serializer.name, recipient.email)
        serializer.save()

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

    def perform_update(self, serializer):
        host = self.request.get_host()
        url = f"https//{host}/materials/course/{self.serializer.pk}"
        recipient_list = serializer.course.subscriptions.user
        for recipient in recipient_list:
            send_email.delay(url, serializer.course.name, recipient.email)
        serializer.save()


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


class PaymentCreate(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated & ~IsModerPermission,)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = get_product(payment.course.name if payment.course else payment.lesson.name)
        price = get_price(payment.amount, product)
        session_id, link = get_session(price)
        payment.session_id = session_id
        payment.link = link
        payment.save()


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

        return Response({"message": message}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
