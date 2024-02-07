import os
from django.conf import settings

from django.dispatch import receiver

from videoflixbackend.tasks import convert_480p, convert_720p, convert_1080p, create_thumbnail
from .models import Video
from django.db.models.signals import post_save, post_delete, pre_save
import django_rq
from django.core.cache import cache


@receiver(post_save, sender =Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('Neues Video erstellt', instance.video_file.path)
        queue = django_rq.get_queue('default',autocommit=True)          
       
        base, _ = os.path.splitext(instance.video_file.path)

        # Fügen Sie den Thumbnail-Erstellungsjob zur Queue hinzu
        thumbnail_output = base + '-thumbnail.jpg'
        queue.enqueue(create_thumbnail, instance.video_file.path, thumbnail_output, instance.id)
              
        #Jobs zur KOnvertierung werden in die queue gestellt
        queue.enqueue(convert_480p, instance.video_file.path, base + '-480p.mp4')
        queue.enqueue(convert_720p, instance.video_file.path, base + '-720p.mp4')
        queue.enqueue(convert_1080p, instance.video_file.path, base + '-1080p.mp4')
       
         #Löschen des Cache
        cache.delete('video_list_cache_key')




@receiver(post_delete, sender = Video)        
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            base, _ = os.path.splitext(instance.video_file.path)
            os.remove(instance.video_file.path)
            os.remove( base + '-720p.mp4')
            os.remove( base + '-480p.mp4')
            os.remove( base + '-1080p.mp4')
            print ('Video wurde gelöscht')   
             #Löschen des Cache
            cache.delete('video_list_cache_key')


@receiver(pre_save, sender = Video)
def video_pre_delete_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Video` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Video.objects.get(pk=instance.pk).video_file
    except Video.DoesNotExist:
        return False

    new_file = instance.video_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
         