from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreate,
    LessonDestroy,
    LessonList,
    LessonRetrieve,
    LessonUpdate, PaymentList, SubscriptionAPIView
)

app_name = MaterialsConfig.name
router = routers.DefaultRouter()
router.register(r"course", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonList.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreate.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/update/", LessonUpdate.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete/", LessonDestroy.as_view(), name="lesson_delete"),
    path("lesson/<int:pk>/retrieve/", LessonRetrieve.as_view(), name="lesson_retrieve"),
    path("payment/", PaymentList.as_view(), name="payment_list"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription")
]
urlpatterns += router.urls
