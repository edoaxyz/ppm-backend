# Generated by Django 4.2.1 on 2023-06-09 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=255)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='FieldAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('mandatory', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('allow_anonymous', models.BooleanField(default=False)),
                ('allow_answer_edits', models.BooleanField(default=True)),
                ('hidden', models.BooleanField(default=True)),
                ('multiple_answers', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='ChoiceAnswer',
            fields=[
                ('fieldanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.fieldanswer')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.fieldanswer',),
        ),
        migrations.CreateModel(
            name='ChoicesQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='FileAnswer',
            fields=[
                ('fieldanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.fieldanswer')),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.fieldanswer',),
        ),
        migrations.CreateModel(
            name='FileQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='MultipleChoiceAnswer',
            fields=[
                ('fieldanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.fieldanswer')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.fieldanswer',),
        ),
        migrations.CreateModel(
            name='OpenQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
                ('placeholder', models.TextField(blank=True, max_length=255, null=True)),
                ('text_limit', models.IntegerField(blank=True, null=True)),
                ('regex_validator', models.CharField(blank=True, max_length=511, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('fieldanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.fieldanswer')),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.fieldanswer',),
        ),
    ]
