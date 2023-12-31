# Generated by Django 4.2 on 2023-04-10 05:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ROMO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=100)),
                ('romo_label', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('last_active', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password_encryted', models.CharField(max_length=100)),
                ('tool_control', models.SmallIntegerField(null=True)),
                ('face_recognize', models.BooleanField(null=True)),
                ('create_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Unauthorized',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unathorized_img_url', models.CharField(max_length=100)),
                ('unknown_img_label', models.CharField(max_length=100)),
                ('capture_datetime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('romo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='live_streaming_v3.romo')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='live_streaming_v3.user')),
            ],
        ),
        migrations.AddField(
            model_name='romo',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='live_streaming_v3.user'),
        ),
        migrations.CreateModel(
            name='Face_Recognize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorized_img_url', models.CharField(max_length=200)),
                ('image_label', models.CharField(max_length=100)),
                ('upload_datatime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='live_streaming_v3.user')),
            ],
        ),
    ]
