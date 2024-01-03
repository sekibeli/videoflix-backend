import os
from django.dispatch import receiver

from videoflixbackend.tasks import convert_480p, convert_720p
from .models import Video
from django.db.models.signals import post_save, post_delete, pre_save
import django_rq

@receiver(post_save, sender =Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('Neues Video erstellt', instance.video_file.path)
        queue = django_rq.get_queue('default',autocommit=True)
          
       
        base, _ = os.path.splitext(instance.video_file.path)
        # new_file_name = base + '-480p.mp4'
        # print('newfilename', new_file_name)
           
        #Job zur KOnvertierung wird in die queue gestellt
       # queue.enqueue(convert_480p, instance.video_file.path)
        queue.enqueue(convert_480p, instance.video_file.path, base + '-480p.mp4')
        queue.enqueue(convert_720p, instance.video_file.path, base + '-720p.mp4')
       



@receiver(post_delete, sender = Video)        
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            base, _ = os.path.splitext(instance.video_file.path)
            os.remove(instance.video_file.path)
            os.remove( base + '-720p.mp4')
            os.remove( base + '-480p.mp4')
            print ('Video wurde gelöscht')   
        


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
         