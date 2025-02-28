# Generated by Django 5.0.6 on 2024-07-03 20:25

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='gameSessionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionId', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('sessionStartTime', models.DateTimeField(auto_now_add=True)),
                ('sessionendTime', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='playerMoveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerMove', models.CharField(max_length=100)),
                ('computerMove', models.CharField(max_length=100)),
                ('gameResult', models.CharField(max_length=100)),
                ('moveRecordTime', models.DateTimeField(auto_now_add=True)),
                ('gameSessionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gamesessionmodel')),
            ],
        ),
    ]
