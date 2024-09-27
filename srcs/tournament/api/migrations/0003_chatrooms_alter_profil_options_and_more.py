# Generated by Django 4.0 on 2024-09-27 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0002_alter_profil_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomName', models.CharField(max_length=100)),
                ('roomActive', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'api_chat_rooms',
            },
        ),
        migrations.AlterModelOptions(
            name='profil',
            options={},
        ),
        migrations.AlterModelOptions(
            name='profilecomment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='userfriendslist',
            options={},
        ),
        migrations.CreateModel(
            name='ChatUserList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chatrooms')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'api_chat_users_list',
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('type', models.CharField(choices=[('chat', 'Chat'), ('activity', 'Activity')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chatRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chatrooms')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'api_chat_message',
            },
        ),
    ]
