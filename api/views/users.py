from rest_framework import viewsets, mixins
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

    def check_object_permissions(self, request, obj):
        if (
            self.action in ["delete", "update", "create", "partial_update"]
            and self.request.user != obj
        ):
            self.permission_denied(request)
        return super().check_object_permissions(request, obj)

    def get_object(self):
        pk = self.kwargs[self.lookup_url_kwarg or self.lookup_field]
        if pk == "me" and self.request.user.is_authenticated:
            return self.request.user
        return super().get_object()
