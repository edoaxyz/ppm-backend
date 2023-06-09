from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SurveyViewSet, UserViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r"survey", SurveyViewSet, basename="survey")
router.register(r"user", UserViewSet, basename="user")
router.register(r"survey/(?P<survey>\d+)/answer", AnswerViewSet, basename="answer")

urlpatterns = [
    path("", include(router.urls)),
]
