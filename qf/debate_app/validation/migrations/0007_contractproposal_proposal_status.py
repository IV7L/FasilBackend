# Generated by Django 4.1.4 on 2023-04-30 02:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("validation", "0006_contractproposal_voting_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="contractproposal",
            name="proposal_status",
            field=models.CharField(
                choices=[
                    ("1", "CREATED"),
                    ("2", "ACTIVE"),
                    ("3", "SUCCEEDED"),
                    ("4", "QUEUED"),
                    ("5", "EXECUTED"),
                ],
                default=1,
                max_length=255,
            ),
            preserve_default=False,
        ),
    ]
