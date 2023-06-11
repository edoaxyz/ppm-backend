from django.urls import reverse
from rest_framework import serializers

from surveys.models import Survey, Question

from .questions import QuestionPolymorphicSerializer
from .list import SurveyListSerializer


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionPolymorphicSerializer(many=True, default=[])
    answers = serializers.SerializerMethodField(read_only=True)

    def _save_questions(self, survey, questions):
        if questions == None:
            return
        ser = QuestionPolymorphicSerializer(context=self.context, partial=self.partial)
        ser.parent = self
        current_questions = {q.id: q for q in survey.questions.all()}
        for i, question in enumerate(questions):
            id = question.get("id")
            if current_questions.get(id):
                inst = current_questions[id]
                del current_questions[id]
                ser.update(inst, {"survey": survey, "order": i, **question})
            else:
                ser.create({"survey": survey, "order": i, **question, "id": None})
        Question.objects.non_polymorphic().filter(
            survey=survey, id__in=current_questions.keys()
        ).delete()

    def create(self, validated_data):
        questions = (
            validated_data.pop("questions") if "questions" in validated_data else None
        )
        survey = super().create(validated_data)
        self._save_questions(survey, questions)
        return survey

    def update(self, instance, validated_data):
        questions = (
            validated_data.pop("questions") if "questions" in validated_data else None
        )
        survey = super().update(instance, validated_data)
        self._save_questions(survey, questions)
        return survey

    def save(self, **kwargs):
        return super().save(author=self.context.get("request").user, **kwargs)

    def get_answers(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse("answer-list", kwargs={"survey": obj.pk})
        )

    class Meta:
        model = Survey
        fields = "__all__"
        read_only_fields = ["author", "date_created", "date_modified"]


class SurveyAnonymousSerializer(SurveyListSerializer):
    questions = QuestionPolymorphicSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        exclude = [
            "allowed_users",
            "allow_anonymous",
            "allow_answer_edits",
            "hidden",
            "multiple_answers",
        ]
