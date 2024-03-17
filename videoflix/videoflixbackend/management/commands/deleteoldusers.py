from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from user.models import CustomUser


class Command(BaseCommand):
    help = 'Löscht alle User-Instanzen, die als Gast markiert sind und vor mehr als 24 Stunden erstellt wurden'

    def handle(self, *args, **kwargs):
        # Definiere den Zeitpunkt, vor dem die User erstellt worden sein müssen, um gelöscht zu werden
        cutoff = timezone.now() - timedelta(hours=0.5)

        # Filtere die User-Instanzen, die gelöscht werden sollen
        users_to_delete = CustomUser.objects.filter(is_guest=True, date_joined__lt=cutoff)

        # Zähle die Anzahl der zu löschenden User
        users_count = users_to_delete.count()

        # Lösche die gefilterten User-Instanzen
        users_to_delete.delete()

        # Gib eine Nachricht aus, die anzeigt, wie viele User gelöscht wurden
        self.stdout.write(self.style.SUCCESS(f'{users_count} Gast-User, die vor mehr als 24 Stunden erstellt wurden, wurden erfolgreich gelöscht.'))
