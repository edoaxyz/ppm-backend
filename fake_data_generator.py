import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polls.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.core.files import File
from faker import Faker
from io import BytesIO
from PIL import Image
from random import randint, choice
from surveys.models import (
    Survey,
    OpenQuestion,
    ChoicesQuestion,
    MultipleChoicesQuestion,
    FileQuestion,
    Choice,
    Question,
)

fake = Faker()
User = get_user_model()

Choice.objects.all().delete()
MultipleChoicesQuestion.objects.non_polymorphic().all().delete()
Question.objects.non_polymorphic().all().delete()
Survey.objects.all().delete()
User.objects.exclude(id=1).delete()

# Generate 5 random users
users = {}
for _ in range(5):
    email = fake.email()
    password = fake.password()
    user = User.objects.create(email=email, password=password)
    user.set_password(password)
    user.save()
    users[f"{email}:{password}"] = user

# Get the user with author_id = 1
author = User.objects.get(id=1)

# Create 10 fake surveys with switching authors
for i in range(10):
    # Choose a random author
    current_author = choice(list(users.values()))

    # Create a survey
    survey = Survey.objects.create(
        title=fake.sentence(),
        author=current_author,
        allow_anonymous=fake.boolean(),
        allow_answer_edits=fake.boolean(),
        hidden=fake.boolean(),
        multiple_answers=fake.boolean(),
    )

    # Generate a fake image file
    image = Image.new("RGB", (800, 600), fake.hex_color())
    image_io = BytesIO()
    image.save(image_io, format="JPEG")
    image_file = File(image_io, name="survey_image.jpg")

    # Set the image field of the survey
    survey.image = image_file
    survey.save()

    # Add allowed users
    if fake.boolean():
        allowed_users = User.objects.exclude(id=current_author.id).order_by("?")[:3]
        survey.allowed_users.set(allowed_users)

    # Create at least 3 questions for the survey
    for _ in range(3):
        question_type = choice(["open", "choices", "multiple_choices", "file"])

        if question_type == "open":
            # Create an open question
            question = OpenQuestion.objects.create(
                survey=survey,
                title=fake.sentence(),
                description=fake.paragraph(),
                mandatory=fake.boolean(),
                placeholder=fake.sentence(),
                text_limit=randint(10, 100),
                regex_validator=None,
            )
        elif question_type == "choices":
            # Create a choices question
            question = ChoicesQuestion.objects.create(
                survey=survey,
                title=fake.sentence(),
                description=fake.paragraph(),
                mandatory=fake.boolean(),
            )

            # Create 3 choices for the question
            for _ in range(3):
                Choice.objects.create(
                    question=question, title=fake.sentence(), order=randint(1, 10)
                )
        elif question_type == "multiple_choices":
            # Create a multiple choices question
            question = MultipleChoicesQuestion.objects.create(
                survey=survey,
                title=fake.sentence(),
                description=fake.paragraph(),
                mandatory=fake.boolean(),
            )

            # Create a random number of choices (between 3 and 7)
            num_choices = randint(3, 7)

            # Create choices for the question
            choices = []
            for i in range(num_choices):
                choice_obj = Choice.objects.create(
                    question=question, title=fake.sentence(), order=i + 1
                )
                choices.append(choice_obj)

            # Set min_selection to a random number less than the number of choices
            min_selection = randint(1, num_choices - 1)
            question.min_selection = min_selection
            question.max_selection = num_choices
            question.save()

        else:
            # Create a file question
            question = FileQuestion.objects.create(
                survey=survey,
                title=fake.sentence(),
                description=fake.paragraph(),
                mandatory=fake.boolean(),
            )

    print(
        f"Survey '{survey.title}' created with {survey.questions.count()} questions. Author: {current_author.email}"
    )

# Print the created users
print("Created Users:")
for k, user in users.items():
    print(k)
