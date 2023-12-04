# Generated by Django 4.2.3 on 2023-12-02 22:18

import autoslug.fields
from django.db import migrations, models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Enquiry",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, verbose_name="Your Name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+2348155200000",
                        max_length=30,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("subject", models.CharField(max_length=100, verbose_name="Subject")),
                ("message", models.TextField(verbose_name="Message")),
                (
                    "is_answered",
                    models.BooleanField(default=False, verbose_name="Is answered"),
                ),
            ],
            options={
                "verbose_name": "Enquiry",
                "verbose_name_plural": "Enquiries",
            },
        ),
    ]