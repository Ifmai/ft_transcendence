# Generated by Django 5.0.6 on 2024-09-01 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userfriendslist'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='is_online',
            field=models.BooleanField(default=False, null=True),
        ),
    ]