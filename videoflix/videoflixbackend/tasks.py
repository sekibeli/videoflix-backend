import subprocess
import os

from django.conf import settings
from .models import Video


def create_thumbnail(source, output, video_id):

    cmd = [
        'ffmpeg',
        '-i', source,
        '-ss', '00:00:01',
        '-vframes', '1',
        '-s', '1280x720',
        output
    ]

    subprocess.run(cmd, capture_output=True)

    thumbnail_rel_path = os.path.relpath(output, settings.MEDIA_ROOT)
    
    video = Video.objects.get(id=video_id)
    video.thumbnail = thumbnail_rel_path
    video.save()


def convert_480p(source, output):
    print('hey convert_480p wird ausgeführt')

    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output
    ]
    run = subprocess.run(cmd, capture_output=True)
  
    
    
    

def convert_720p(source, output):
           
        cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output
    ]
        run = subprocess.run(cmd, capture_output=True)


def convert_1080p(source, output):
           
        cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd1080',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        output
    ]
        run = subprocess.run(cmd, capture_output=True)