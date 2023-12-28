# Generated by Django 4.2.3 on 2023-12-28 00:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="salary",
            field=models.CharField(
                choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
                default="Low",
                max_length=20,
                verbose_name="Salary",
            ),
        ),
    ]