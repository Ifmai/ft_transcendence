# Generated by Django 4.0 on 2024-09-18 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('round', models.IntegerField(default=1)),
                ('state', models.CharField(choices=[('PLY', 'PLAYED'), ('UPL', 'UNPLAYED')], default='UPL', max_length=3)),
            ],
            options={
                'db_table': 'api_match',
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=120, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profil_photo/%Y/%m/')),
                ('two_factory', models.BooleanField(default=False)),
                ('otp_secret_key', models.CharField(blank=True, max_length=64, null=True)),
                ('alias_name', models.CharField(blank=True, max_length=100, null=True)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('ON', 'ONLINE'), ('OF', 'OFFLINE'), ('IG', 'INGAME')], default='OF', max_length=2)),
                ('championships', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to='auth.user')),
            ],
            options={
                'verbose_name_plural': 'Profils',
                'db_table': 'api_profil',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('round', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('PN', 'PENDING'), ('PG', 'IN_PROGRESS'), ('FN', 'FINISHED')], default='PN', max_length=2)),
            ],
            options={
                'db_table': 'api_tournament',
            },
        ),
        migrations.CreateModel(
            name='ProfileComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=300)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('user_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.profil')),
            ],
            options={
                'verbose_name_plural': 'ProfileCommand',
                'db_table': 'api_profil_comment',
            },
        ),
        migrations.CreateModel(
            name='PlayerTournament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creator', models.BooleanField(default=False)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.profil')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tournament')),
            ],
            options={
                'db_table': 'api_player_tournament',
            },
        ),
        migrations.CreateModel(
            name='PlayerMatch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('won', models.BooleanField(default=False)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.profil')),
            ],
            options={
                'db_table': 'api_player_match',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.tournament'),
        ),
        migrations.CreateModel(
            name='UserFriendsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_request', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_friend_requests', to='auth.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_friend_requests', to='auth.user')),
            ],
            options={
                'verbose_name_plural': 'UserFriendsList',
                'db_table': 'api_user_friend_list',
                'unique_together': {('sender', 'receiver')},
            },
        ),
    ]
