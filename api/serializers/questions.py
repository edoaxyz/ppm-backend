from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from surveys.models import (
    Question,
    OpenQuestion,
    FileQuestion,
    Choice,
    ChoicesQuestion,
    MultipleChoicesQuestion,
)


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ["id", "title", "description", "mandatory"]


class OpenQuestionSerializer(QuestionSerializer):
    class Meta:
        model = OpenQuestion
        fields = [
            "id",
            "title",
            "description",
            "mandatory",
            "placeholder",
            "text_limit",
            "regex_validator",
        ]


class FileQuestionSerializer(QuestionSerializer):
    class Meta:
        model = FileQuestion
        fields = ["id", "title", "description", "mandatory"]


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = ["id", "title"]


class ChoicesQuestionSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True)

    def _get_child_serializer(self):
        ser = ChoiceSerializer(context=self.context, partial=self.partial)
        ser.parent = self
        return ser

    def _save_choices(self, question, choices):
        if choices:
            existing_choices = {c.id: c for c in question.choices.all()}
            ser = self._get_child_serializer()
            for i, c in enumerate(choices):
                id = c.get("id")
                if existing_choices.get(id):
                    inst = existing_choices[id]
                    del existing_choices[id]
                    ser.update(inst, {"question": question, "order": i, **c})
                else:
                    ser.create({"question": question, "order": i, **c, "id": None})
            Choice.objects.filter(
                question=question, id__in=existing_choices.keys()
            ).delete()

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        question = super().create(validated_data)
        self._save_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices")
        question = super().update(instance, validated_data)
        self._save_choices(question, choices)
        return question

    class Meta:
        model = ChoicesQuestion
        fields = ["id", "title", "description", "mandatory", "choices"]


class MultipleChoicesQuestionSerializer(ChoicesQuestionSerializer):
    class Meta:
        model = MultipleChoicesQuestion
        fields = [
            "id",
            "title",
            "description",
            "mandatory",
            "choices",
            "min_selection",
            "max_selection",
        ]


class QuestionPolymorphicSerializer(PolymorphicSerializer):
    id = serializers.IntegerField(required=False)

    model_serializer_mapping = {
        OpenQuestion: OpenQuestionSerializer,
        FileQuestion: FileQuestionSerializer,
        ChoicesQuestion: ChoicesQuestionSerializer,
        MultipleChoicesQuestion: MultipleChoicesQuestionSerializer,
    }
