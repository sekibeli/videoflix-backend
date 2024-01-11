import os
from django.dispatch import receiver

from videoflixbackend.tasks import convert_480p, convert_720p, convert_1080p
from .models import Video
from django.db.models.signals import post_save, post_delete, pre_save
import django_rq

# These imports sare for the passwort reset logic from DRF 
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save, sender =Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('Neues Video erstellt', instance.video_file.path)
        queue = django_rq.get_queue('default',autocommit=True)
          
       
        base, _ = os.path.splitext(instance.video_file.path)
              
        #Jobs zur KOnvertierung werden in die queue gestellt
        queue.enqueue(convert_480p, instance.video_file.path, base + '-480p.mp4')
        queue.enqueue(convert_720p, instance.video_file.path, base + '-720p.mp4')
        queue.enqueue(convert_1080p, instance.video_file.path, base + '-1080p.mp4')
       



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
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
         
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Password Reset for Videoflix"),
        # message:
        email_plaintext_message,
        # from: Hier sollte später eine richtige Email stehen
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
