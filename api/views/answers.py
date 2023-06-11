from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from django.db.models import Q

from surveys.models import Answer, Survey
from ..serializers import AnswerSerializer


class AnswerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_survey(self):
        if not getattr(self, "_survey", None):
            survey_pk = self.kwargs.get("survey")
            self._survey = get_object_or_404(Survey, pk=survey_pk)
        return self._survey

    def get_permissions(self):
        if self.action == "create":
            return super().get_permissions()
        return super().get_permissions() + [permissions.IsAuthenticated()]

    def check_permissions(self, request):
        survey = self.get_survey()
        if survey.author == request.user:
            return super().check_permissions(request)
        if survey.allowed_users.count() > 0 and not survey.allowed_users.contains(
            request.user
        ):
            self.permission_denied(request, "You are not allowed to answer this survey")
        elif not survey.allow_anonymous and not request.user.is_authenticated:
            self.permission_denied(
                request, "You must be authenticated to answer this survey"
            )
        elif (
            self.action == "update" or self.action == "partial_update"
        ) and not survey.allow_answer_edits:
            self.permission_denied(request, "Answers to this survey cannot be edited")
        elif (
            self.action == "create"
            and not survey.multiple_answers
            and request.user.is_authenticated
            and survey.answers.filter(user=request.user)
        ):
            self.permission_denied(
                request, "You already gave an answer for this survey"
            )
        return super().check_permissions(request)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(survey=self.get_survey())
                & (Q(user=self.request.user) | Q(survey__author=self.request.user))
            )
        ).order_by("-date_created")

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(
            *args, survey_instance=self.get_survey(), **kwargs
        )
