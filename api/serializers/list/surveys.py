
from rest_framework import serializers

from surveys.models import Survey

class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        exclude = [
            "allowed_users",
            "allow_anonymous",
            "allow_answer_edits",
            "hidden",
            "multiple_answers",
        ]
