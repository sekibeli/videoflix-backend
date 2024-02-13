# Generated by Django 5.0 on 2024-02-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflixbackend', '0014_alter_video_thumbnail_alter_video_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
