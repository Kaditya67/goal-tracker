# Generated by Django 5.1.1 on 2024-09-21 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('progress', models.CharField(max_length=100)),
                ('messages', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='YouTubePlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('playlist_id', models.CharField(max_length=100, unique=True)),
                ('playlist_url', models.URLField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='YouTubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('thumbnail_url', models.URLField()),
                ('watched', models.BooleanField(default=False)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='youtube_track.youtubeplaylist')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VideoFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='youtube_track.youtubevideo')),
            ],
        ),
    ]
