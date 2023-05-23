# Generated by Django 4.1.4 on 2023-04-28 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("debate_app", "0002_initial"),
        ("validation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VoteProposal",
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
                ("proposal_id", models.CharField(max_length=255)),
                ("provider", models.CharField(max_length=255)),
                ("signer", models.CharField(max_length=255)),
                ("governor", models.CharField(max_length=255)),
                ("vote_way", models.CharField(max_length=255)),
                ("reaseon", models.CharField(max_length=255)),
                ("governor_state_after_vote", models.CharField(max_length=255)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "debate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="debate_app.debate",
                    ),
                ),
            ],
        ),
    ]