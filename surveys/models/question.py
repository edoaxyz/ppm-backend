from django.db import models
from polymorphic.models import PolymorphicModel

from .survey import Survey
from .utils import NON_POLYMORPHIC_CASCADE


class Question(PolymorphicModel):
    order = models.IntegerField(default=0)
    survey = models.ForeignKey(
        Survey, related_name="questions", on_delete=NON_POLYMORPHIC_CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    mandatory = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order",)


class OpenQuestion(Question):
    placeholder = models.TextField(max_length=255, null=True, blank=True)
    text_limit = models.IntegerField(null=True, blank=True)
    regex_validator = models.CharField(max_length=511, null=True, blank=True)


class ChoicesQuestion(Question):
    pass


class Choice(models.Model):
    title = models.TextField(max_length=255)
    order = models.IntegerField(default=0)
    question = models.ForeignKey(
        ChoicesQuestion, related_name="choices", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order",)


class MultipleChoicesQuestion(ChoicesQuestion):
    min_selection = models.IntegerField(null=True, blank=True)
    max_selection = models.IntegerField(null=True, blank=True)


class FileQuestion(Question):
    pass
