# Generated by Django 4.2 on 2023-06-04 11:08

from django.db import migrations

def set_default_value(apps, schema_editor):
    AuthorizedImg = apps.get_model('authorized', 'AuthorizedImg')
    AuthorizedImg.objects.filter(authorized_img=None).update(authorized_img='default_value')

class Migration(migrations.Migration):
    dependencies = [
        ("authorized", "0001_initial"),
    ]

    operations = []
