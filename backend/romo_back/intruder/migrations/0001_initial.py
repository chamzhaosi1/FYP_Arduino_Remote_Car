# Generated by Django 4.2 on 2023-06-07 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import intruder.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IntruderImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intruder_img', models.ImageField(upload_to=intruder.models.get_image_path)),
                ('uploaded_datetime', models.DateTimeField()),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
