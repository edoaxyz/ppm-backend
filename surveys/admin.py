from django.contrib import admin
from django.db import models
from django.forms import TextInput
import nested_admin

from surveys.models import (
    Survey,
    Question,
    OpenQuestion,
    ChoicesQuestion,
    Choice,
    MultipleChoicesQuestion,
    FileQuestion,
    Answer,
    FieldAnswer,
    TextAnswer,
    FileAnswer,
    ChoiceAnswer,
    MultipleChoiceAnswer,
)


class QuestionInline(nested_admin.NestedStackedPolymorphicInline):
    class OpenQuestionInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = OpenQuestion

    class ChoicesQuestionInline(nested_admin.NestedStackedPolymorphicInline.Child):
        class ChoiceInline(nested_admin.NestedTabularInline):
            model = Choice
            formfield_overrides = {
                models.TextField: {"widget": TextInput(attrs={"rows": "1"})},
            }
            extra = 0

        model = ChoicesQuestion
        inlines = (ChoiceInline,)

    class MultipleChoicesQuestionInline(ChoicesQuestionInline):
        model = MultipleChoicesQuestion

    class FileQuestionInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = FileQuestion

    model = Question
    child_inlines = (
        OpenQuestionInline,
        ChoicesQuestionInline,
        MultipleChoicesQuestionInline,
        FileQuestionInline,
    )


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    readonly_fields = ("user", "date_created", "date_modified")
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


@admin.register(Survey)
class SurveyAdmin(
    nested_admin.NestedPolymorphicInlineSupportMixin, nested_admin.NestedModelAdmin
):
    inlines = (QuestionInline, AnswerInline)
    list_display = ("title", "author", "date_created", "date_modified")


class FieldAnswerInline(nested_admin.NestedStackedPolymorphicInline):
    class TextAnswerInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = TextAnswer

    class ChoiceAnswerInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = ChoiceAnswer

    class MultipleChoiceAnswerInline(ChoiceAnswerInline):
        model = MultipleChoiceAnswer

    class FileAnswerInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = FileAnswer

    model = FieldAnswer
    child_inlines = (
        TextAnswerInline,
        ChoiceAnswerInline,
        MultipleChoiceAnswerInline,
        FileAnswerInline,
    )


@admin.register(Answer)
class AnswerAdmin(
    nested_admin.NestedPolymorphicInlineSupportMixin, nested_admin.NestedModelAdmin
):
    inlines = (FieldAnswerInline,)
    pass
