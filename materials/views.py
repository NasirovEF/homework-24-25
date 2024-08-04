from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from materials.models import Course, Lesson, Payment
from materials.permissions import IsModerPermission, IsOwnerPermission
from materials.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerPermission | IsOwnerPermission,)


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & ~IsModerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerPermission | IsOwnerPermission,)


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated & IsOwnerPermission,)


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course', 'lesson', 'pay_method')
    ordering_fields = ('-pay_date',)
