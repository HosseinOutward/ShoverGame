# Generated by Django 3.2.7 on 2021-09-03 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_profile', models.ImageField(default='profile_pic/default.jpg', upload_to='profile_pic')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreBoardEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highScore_score', models.IntegerField(default=-1)),
                ('highFortune_score', models.IntegerField(default=-1)),
                ('time_played_score', models.FloatField(default=-1)),
                ('start_time_score', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_time_score', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_score', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
