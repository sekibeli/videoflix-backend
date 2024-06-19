from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv()
from rq import Retry
from django.dispatch import receiver

from videoflixbackend.tasks import  convert_and_save_quality, create_thumbnail
from .models import Video, VideoQuality
from django.db.models.signals import post_save, post_delete, pre_save
import django_rq
from django.core.cache import cache
from django.core.mail import send_mail
from user.models import CustomUser



# These imports sare for the passwort reset logic from DRF 
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    cache.delete('video_list_cache_key')
    cache.delete('videos_today_cache_key')
    cache.delete('videos_yesterday_cache_key')
    cache.delete('recent_videos_cache_key')
    cache.delete('popular_videos_cache_key')
    cache.delete('most_seen_videos_cache_key')
    if created:
        queue = django_rq.get_queue('default',autocommit=True)          
       

        thumbnail_output = f'thumbnails/{instance.id}-thumbnail.jpg'
        queue.enqueue(create_thumbnail, instance.video_file.path, thumbnail_output, instance.id)
              
        queue.enqueue(convert_and_save_quality, instance, '360px', '480x360', retry=Retry(max=5, interval=[10, 30, 60, 120, 300]))
        queue.enqueue(convert_and_save_quality, instance,  '720p', '1280x720', retry=Retry(max=5, interval=[10, 30, 60, 120, 300]))
        queue.enqueue(convert_and_save_quality, instance,'1080p', '1920x1080', retry=Retry(max=5, interval=[10, 30, 60, 120, 300]))

         # E-Mail an (alle) Superuser senden
        subject = 'Neues Video hochgeladen'
        message = f'Ein neues Video mit dem Titel "{instance.title}" wurde hochgeladen und wartet auf Überprüfung.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        send_mail(subject, message, email_from, recipient_list)
       
         #Löschen des Cache
    cache.delete('video_list_cache_key')


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    cache.delete('video_list_cache_key')
    cache.delete('videos_today_cache_key')
    cache.delete('videos_yesterday_cache_key')
    cache.delete('recent_videos_cache_key')
    cache.delete('popular_videos_cache_key')
    cache.delete('most_seen_videos_cache_key')

    if instance.video_file:
        base, ext = os.path.splitext(instance.video_file.path)
        
        files_to_delete = [
            instance.video_file.path,
            f'{base}-360px{ext}',
            f'{base}-480p{ext}',
            f'{base}-720p{ext}',
            f'{base}-1080p{ext}'
        ]

        for file_path in files_to_delete:
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Löschen der zugehörigen Einträge in der VideoQuality-Tabelle
        VideoQuality.objects.filter(video=instance).delete()
        print('Video und Qualitätsvideos wurden gelöscht')



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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_password_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_password_token.key}"

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': reset_password_url
    }

    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)

         
    msg = EmailMultiAlternatives(
        "Password Reset for {title}".format(title="Password Reset for Videoflix"),
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
