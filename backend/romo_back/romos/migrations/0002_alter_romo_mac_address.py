# Generated by Django 4.2 on 2023-04-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("romos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="romo",
            name="mac_address",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
