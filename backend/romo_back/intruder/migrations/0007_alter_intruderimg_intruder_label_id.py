# Generated by Django 4.2 on 2023-06-08 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intruder", "0006_alter_intruderimg_intruder_label_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="intruderimg",
            name="intruder_label_id",
            field=models.CharField(max_length=100),
        ),
    ]
