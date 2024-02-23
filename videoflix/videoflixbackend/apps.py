from django.apps import AppConfig


class VideoflixbackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoflixbackend'


    def ready(self):
        from django.utils import timezone
        from django_rq import get_scheduler
        from .tasks import delete_inactive_guest_users
        scheduler = get_scheduler('default')
        scheduler.schedule(
            scheduled_time=timezone.now(), 
            func='videoflixbackend.tasks.delete_inactive_guest_users',
            interval=86400, 
        )
