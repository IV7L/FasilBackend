# Generated by Django 4.1.4 on 2023-05-05 02:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("validation", "0012_alter_debatearg_opposing_quote_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractproposal",
            name="voting_status",
            field=models.BooleanField(default=True),
        ),
    ]
