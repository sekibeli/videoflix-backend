# Generated by Django 5.0 on 2024-01-25 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_liked_videos'),
        ('videoflixbackend', '0004_alter_video_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='liked_videos',
            field=models.ManyToManyField(blank=True, related_name='liked_videos', to='videoflixbackend.video'),
        ),
    ]
