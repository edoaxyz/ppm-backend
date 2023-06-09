from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from surveys.models import Survey

from ..serializers import SurveyDetailSerializer, SurveyListSerializer, SurveyAnonymousSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list":
            qs = qs.exclude(hidden=True)
        if not self.request.user.is_authenticated:
            qs = qs.filter(allow_anonymous=True, allowed_users=None)
        else:
            qs = qs.exclude(
                ~Q(author=self.request.user)
                & ~Q(allowed_users=None)
                & ~Q(allowed_users__in=[self.request.user])
            )
        qs = qs.order_by("-date_created")
        return qs

    def get_serializer_class(self):
        cls = super().get_serializer_class()
        if self.action == "list":
            return SurveyListSerializer
        if not self.request.user.is_authenticated:
            return SurveyAnonymousSerializer
        return cls

    def get_permissions(self):
        perms = super().get_permissions()
        if self.action in ["delete", "create"]:
            perms += [IsAuthenticated()]
        return perms

    def check_object_permissions(self, request, obj):
        if (
            self.action in ["update", "partial_update", "delete"]
            and self.request.user != obj.author
        ):
            self.permission_denied(request, "You are not allowed to edit this survey")
        return super().check_object_permissions(request, obj)
