# Generated by Django 4.1.4 on 2023-05-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("validation", "0007_contractproposal_proposal_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractproposal",
            name="proposal_args",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
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
                default="1",
                max_length=255,
            ),
        ),
    ]
