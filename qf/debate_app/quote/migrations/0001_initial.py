# Generated by Django 4.1.4 on 2023-04-20 01:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("debate_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuoteBoxCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="RecessRoomQuote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "father",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecessRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("1", "Start Recess"), ("2", "Middle Recess")],
                        max_length=255,
                    ),
                ),
                (
                    "debate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="debate_app.debate",
                    ),
                ),
                ("members", models.ManyToManyField(to="account.debatemember")),
                ("quote", models.ManyToManyField(to="quote.recessroomquote")),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DebateQuote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        validators=[
                            django.core.validators.MaxLengthValidator(500),
                            django.core.validators.MinLengthValidator(50),
                        ]
                    ),
                ),
                ("validated", models.BooleanField(default=False)),
                ("NFTed", models.BooleanField(default=False)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("1", "Supporting Quote"),
                            ("2", "Opposing Quote"),
                            ("3", "Rebuttal Conflict Quote"),
                            ("4", "Rebuttal Description Quote"),
                            ("5", "Rebuttal Question Quote"),
                            ("6", "Rebuttal Question Answer Quote"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "debate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="debate_app.debate",
                    ),
                ),
                (
                    "father",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]