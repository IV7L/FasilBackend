# Generated by Django 4.1.4 on 2023-04-30 02:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("validation", "0005_contractproposal_team1_voting_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contractproposal",
            name="voting_status",
            field=models.BooleanField(default=False),
        ),
    ]
