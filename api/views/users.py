from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login

from users.models import User
from ..serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"])
    def login(self, request):
        if request.data.get("email") and request.data.get("password"):
            user = authenticate(
                request,
                email=request.data.get("email"),
                password=request.data.get("password"),
            )
            if user is not None:
                login(request, user)
                return Response(status=200)
        return Response(status=403)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        self.kwargs["pk"] = request.user.id
        return self.retrieve(request)

    def check_object_permissions(self, request, obj):
        if (
            self.action in ["delete", "update", "create", "partial_update"]
            and self.request.user != obj
        ):
            self.permission_denied(request)
        return super().check_object_permissions(request, obj)
