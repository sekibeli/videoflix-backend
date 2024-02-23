import subprocess
import os

from django.conf import settings

from user.models import CustomUser
from .models import Video

from django.utils import timezone
from datetime import timedelta


def create_thumbnail(source, output, video_id):
    base_dir = os.path.join(settings.MEDIA_ROOT)
    thumbnail_dir = os.path.join(base_dir, 'thumbnails')  
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir) 

    thumbnail_base_name = os.path.basename(output)
    thumbnail_path = os.path.join(thumbnail_dir, thumbnail_base_name)

    cmd = [
        'ffmpeg',
        '-i', source,
        '-ss', '00:00:01',
        '-vframes', '1',
        '-s', '1280x720',
        thumbnail_path  
    ]

    subprocess.run(cmd, capture_output=True)

    thumbnail_rel_path = os.path.join('thumbnails', thumbnail_base_name)
    video = Video.objects.get(id=video_id)
    video.thumbnail.name = thumbnail_rel_path
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


def delete_inactive_guest_users():
    time_threshold = timezone.now() - timedelta(hours=24)
    inactive_guests = CustomUser.objects.filter(updated_at__lt=time_threshold, is_guest=True)

    for guest in inactive_guests:
        Video.objects.filter(created_from=guest).delete()
    count = inactive_guests.count()
    inactive_guests.delete()
    print(f"Deleted {count} inactive guest users.")

