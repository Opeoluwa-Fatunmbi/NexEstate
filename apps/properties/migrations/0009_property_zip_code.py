# Generated by Django 4.2.3 on 2023-12-19 14:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0008_property_property_valuation_report"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="zip_code",
            field=models.CharField(
                default="10123", max_length=100, verbose_name="Zip Code"
            ),
        ),
    ]
