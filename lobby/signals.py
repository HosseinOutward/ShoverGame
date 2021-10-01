from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Lobby


@receiver(post_save, sender=User)
def create_lobby(sender, instance, created, **kwargs):
    if created:
        instance.last_move_player = instance.player_1_lobby
        # instance.player_1_lobby.epoch_sync_num_plobby = 0
        instance.save()
