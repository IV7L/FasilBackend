# Generated by Django 4.1.4 on 2023-05-21 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("debate_app", "0002_initial"),
        ("validation", "0013_alter_contractproposal_voting_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="DAOArgs",
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
                ("governance_maxSupply", models.IntegerField(default=500)),
                ("governor_quorumPercentage", models.IntegerField(default=51)),
                ("governor_votingDelay", models.IntegerField(default=0)),
                ("governor_votingPeriod", models.IntegerField(default=0)),
                ("governor_proposalThreshold", models.IntegerField(default=0)),
                ("timelock_minDelay", models.IntegerField(default=0)),
                ("box_value", models.CharField(max_length=255)),
                ("box_owner", models.CharField(max_length=255)),
                ("settings_transferAmount", models.IntegerField(default=1)),
                ("settings_deployer", models.CharField(max_length=255)),
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
