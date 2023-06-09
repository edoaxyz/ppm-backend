from django.db import models
from django.contrib.auth import get_user_model


class Survey(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="surveys"
    )
    allowed_users = models.ManyToManyField(
        get_user_model(), blank=True, related_name="shared_surveys"
    )
    allow_anonymous = models.BooleanField(default=False)
    allow_answer_edits = models.BooleanField(default=True)
    hidden = models.BooleanField(default=True)
    multiple_answers = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-date_created",)
