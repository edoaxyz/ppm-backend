from django.db import models
from django.contrib.auth import get_user_model
from polymorphic.models import PolymorphicModel

from .survey import Survey
from .question import (
    OpenQuestion,
    FileQuestion,
    Choice,
    ChoicesQuestion,
    MultipleChoicesQuestion,
)
from .utils import NON_POLYMORPHIC_CASCADE


class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(
        get_user_model(), null=True, related_name="answers", on_delete=models.SET_NULL
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.survey} compiled by {self.user} at {self.date_created}"


class FieldAnswer(PolymorphicModel):
    answer = models.ForeignKey(Answer, on_delete=NON_POLYMORPHIC_CASCADE, related_name="fields")


class TextAnswer(FieldAnswer):
    text = models.TextField()
    field = models.ForeignKey(
        OpenQuestion, related_name="field_answers", on_delete=models.CASCADE
    )


class FileAnswer(FieldAnswer):
    file = models.FileField()
    field = models.ForeignKey(
        FileQuestion, related_name="field_answers", on_delete=models.CASCADE
    )


class ChoiceAnswer(FieldAnswer):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    field = models.ForeignKey(
        ChoicesQuestion, related_name="field_answers", on_delete=models.CASCADE
    )


class MultipleChoiceAnswer(FieldAnswer):
    choices = models.ManyToManyField(Choice)
    field = models.ForeignKey(
        MultipleChoicesQuestion,
        related_name="multiple_field_answers",
        on_delete=models.CASCADE,
    )
