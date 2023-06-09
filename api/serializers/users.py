from rest_framework import serializers

from users.models import User

from .list import SurveyListSerializer,AnswerListSerializer


class UserSerializer(serializers.ModelSerializer):
    my_surveys = SurveyListSerializer(source="surveys", many=True, read_only=True)
    shared_surveys = SurveyListSerializer(many=True, read_only=True)
    answers = AnswerListSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        ret = super().save(**kwargs)
        if "password" in self.validated_data:
            ret.set_password(self.validated_data["password"])
            ret.save()
        return ret

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "picture",
            "date_joined",
            "my_surveys",
            "shared_surveys",
            "answers"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "date_joined": {"read_only": True},
        }
