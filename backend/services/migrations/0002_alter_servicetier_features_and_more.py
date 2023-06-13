# Generated by Django 4.1.3 on 2023-06-12 21:43

import backend.customs
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicetier",
            name="features",
            field=backend.customs.CustomManyToManyField(
                blank=True,
                help_text="Service Tier Features",
                related_name="features",
                to="services.feature",
                verbose_name="Features",
            ),
        ),
        migrations.AlterField(
            model_name="servicetier",
            name="supported_sites",
            field=backend.customs.CustomManyToManyField(
                blank=True,
                help_text="Service Tier Supported Sites",
                related_name="supportedsites",
                to="services.supportedsites",
                verbose_name="Supported Sites",
            ),
        ),
    ]