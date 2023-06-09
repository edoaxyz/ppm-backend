from rest_framework import serializers

from surveys.models import Answer
from .surveys import SurveyListSerializer


class AnswerListSerializer(serializers.ModelSerializer):
    survey = SurveyListSerializer()

    class Meta:
        model = Answer
        fields = ["id", "date_created", "date_modified", "survey"]
        read_only_fields = ["date_created", "date_modified", "survey"]
