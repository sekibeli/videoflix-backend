# Generated by Django 5.0 on 2024-01-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflixbackend', '0003_remove_video_likes_video_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]