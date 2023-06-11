from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from surveys.models import (
    Survey,
    OpenQuestion,
    FileQuestion,
    ChoicesQuestion,
    MultipleChoicesQuestion,
    Choice,
    ChoiceAnswer,
    MultipleChoiceAnswer,
)


class TextReportSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return obj.field_answers.values_list("text", flat=True)

    class Meta:
        model = OpenQuestion
        fields = ["id", "title", "answers"]


class FileReportSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    def get_files(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(f.file.url) for f in obj.field_answers.all()]

    class Meta:
        model = FileQuestion
        fields = ["id", "title", "files"]


class ChoicesQuestionSerializer(serializers.ModelSerializer):
    class ChoiceSerializer(serializers.ModelSerializer):
        total = serializers.SerializerMethodField()
        percentage = serializers.SerializerMethodField()

        def get_total(self, obj):
            return ChoiceAnswer.objects.filter(choice=obj).count()

        def get_percentage(self, obj):
            total = obj.question.field_answers.count()
            if total == 0:
                return 0
            return ChoiceAnswer.objects.filter(choice=obj).count() / total * 100

        class Meta:
            model = Choice
            fields = ["id", "title", "total", "percentage"]

    choices = ChoiceSerializer(many=True)
    total_answers = serializers.SerializerMethodField()

    def get_total_answers(self, obj):
        return obj.field_answers.count()

    class Meta:
        model = ChoicesQuestion
        fields = ["id", "title", "choices", "total_answers"]


class MulitpleChoicesQuestionSerializer(serializers.ModelSerializer):
    class ChoiceSerializer(serializers.ModelSerializer):
        total = serializers.SerializerMethodField()
        percentage = serializers.SerializerMethodField()

        def get_total(self, obj):
            return MultipleChoiceAnswer.objects.filter(choices__in=[obj]).count()

        def get_percentage(self, obj):
            total = obj.question.multiple_field_answers.count()
            if total == 0:
                return 0
            return (
                MultipleChoiceAnswer.objects.filter(choices__in=[obj]).count()
                / total
                * 100
            )

        class Meta:
            model = Choice
            fields = ["id", "title", "total", "percentage"]

    choices = ChoiceSerializer(many=True)
    total_answers = serializers.SerializerMethodField()

    def get_total_answers(self, obj):
        return obj.multiple_field_answers.count()

    class Meta:
        model = MultipleChoicesQuestion
        fields = ["id", "title", "choices", "total_answers"]


class QuestionReportSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        OpenQuestion: TextReportSerializer,
        FileQuestion: FileReportSerializer,
        ChoicesQuestion: ChoicesQuestionSerializer,
        MultipleChoicesQuestion: MulitpleChoicesQuestionSerializer,
    }


class ReportSerializer(serializers.ModelSerializer):
    total_answers = serializers.SerializerMethodField()
    questions = QuestionReportSerializer(many=True, read_only=True)

    def get_total_answers(self, obj):
        return obj.answers.count()

    class Meta:
        model = Survey
        fields = ["total_answers", "questions"]
