from rest_framework import serializers
from django.core.validators import RegexValidator

from surveys.models import (
    Answer,
    FieldAnswer,
    TextAnswer,
    MultipleChoiceAnswer,
    FileAnswer,
    FileQuestion,
    OpenQuestion,
    MultipleChoicesQuestion,
    ChoicesQuestion,
    Choice,
    ChoiceAnswer,
)
from .list import UserListSerializer


class FieldAnswerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self._field = kwargs.pop("field", None)
        super().__init__(*args, **kwargs)
        self.required = self._field.mandatory

    class Meta:
        model = FieldAnswer


class TextAnswerSerializer(FieldAnswerSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields["text"].required = self._field.mandatory
        fields["text"].allow_blank = not self._field.mandatory
        fields["text"].label = self._field.title
        fields["text"].help_text = self._field.description
        if self._field.text_limit:
            fields["text"].max_length = self._field.text_limit
        if self._field.regex_validator:
            fields["text"].validators.append(
                RegexValidator(self._field.regex_validator)
            )
        return fields

    class Meta:
        model = TextAnswer
        fields = ["text"]


class MultipleChoiceAnswerSerializer(FieldAnswerSerializer):
    choices = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Choice.objects.all()
    )

    def get_fields(self):
        fields = super().get_fields()
        fields["choices"].queryset = self._field.choices.all()
        fields["choices"].required = self._field.mandatory
        fields["choices"].label = self._field.title
        fields["choices"].help_text = self._field.description
        return fields

    def validate_choices(self, value):
        if self._field.min_selection and len(value) < self._field.min_selection:
            raise serializers.ValidationError(
                f"Please select at least {self._field.min_selection} choices"
            )
        if self._field.max_selection and len(value) > self._field.max_selection:
            raise serializers.ValidationError(
                f"Please select at most {self._field.max_selection} choices"
            )
        return value

    class Meta:
        model = MultipleChoiceAnswer
        fields = ["choices"]


class ChoiceAnswerSerializer(FieldAnswerSerializer):
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    def get_fields(self):
        fields = super().get_fields()
        fields["choice"].queryset = self._field.choices.all()
        fields["choice"].required = self._field.mandatory
        fields["choice"].label = self._field.title
        fields["choice"].help_text = self._field.description
        return fields

    class Meta:
        model = ChoiceAnswer
        fields = ["choice"]


class FileAnswerSerializer(FieldAnswerSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields["file"].required = self._field.mandatory
        fields["file"].label = self._field.title
        fields["file"].help_text = self._field.description
        return fields

    class Meta:
        model = FileAnswer
        fields = ["file"]


class AnswerSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class AnswerFieldsSerializer(serializers.Serializer):
        def get_fields(self):
            return {
                **super().get_fields(),
                **{
                    str(f.pk): {
                        OpenQuestion: TextAnswerSerializer,
                        FileQuestion: FileAnswerSerializer,
                        ChoicesQuestion: ChoiceAnswerSerializer,
                        MultipleChoicesQuestion: MultipleChoiceAnswerSerializer,
                    }[type(f)](
                        field=f,
                        context=self.context,
                        label=f.title,
                    )
                    for f in self.parent._survey_instance.questions.all()
                },
            }

        def create(self, answer, validated_data):
            for k, v in validated_data.items():
                if len(v) != 0:
                    self.fields[k].create({**v, "answer": answer, "field_id": k})

        def update(self, answer, validated_data):
            existing = {a.field.pk: a for a in answer.fields.all()}
            for k, v in validated_data.items():
                if k in existing:
                    self.fields[k].update(
                        self.existing[k], {**v, "answer": answer, "field_id": k}
                    )
                else:
                    self.fields[k].create({**v, "answer": answer, "field_id": k})

        def to_representation(self, instance):
            return {
                str(k): v.to_representation(instance[int(k)])
                if int(k) in instance
                else None
                for k, v in self.fields.items()
            }

    field_answers = AnswerFieldsSerializer()

    def __init__(self, *args, **kwargs):
        self._survey_instance = kwargs.pop("survey_instance", None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        field_answers = validated_data.pop("field_answers")
        r = super().create(validated_data)
        self.fields["field_answers"].create(r, field_answers)
        return r

    def update(self, instance, validated_data):
        field_answers = validated_data.pop("field_answers")
        r = super().update(instance, validated_data)
        self.fields["field_answers"].update(r, field_answers)
        return r

    def save(self, **kwargs):
        return super().save(
            survey=self._survey_instance,
            user=self.context["request"].user
            if self.context["request"].user.is_authenticated
            else None,
            **kwargs,
        )

    def to_representation(self, instance):
        instance.field_answers = {a.field.pk: a for a in instance.fields.all()}
        return super().to_representation(instance)

    def get_fields(self):
        fields = super().get_fields()
        if self.context["request"].user != self._survey_instance.author:
            del fields["user"]
        return fields

    class Meta:
        model = Answer
        fields = ["id", "user", "date_created", "date_modified", "field_answers"]
        read_only_fields = ["user", "date_created", "date_modified"]
