# Generated by Django 4.1.4 on 2023-04-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quote", "0003_alter_debatequote_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="debatequote",
            name="num",
            field=models.IntegerField(default=0),
        ),
    ]