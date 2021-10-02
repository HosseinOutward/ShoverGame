from django.db import models
from django.contrib.auth.models import User
from os import path
from ShoverGame.settings import MEDIA_ROOT


class MapLayout(models.Model):
    premade_map_hash = models.JSONField(default=dict)
    premade_map_n = models.IntegerField()
    premade_map_m = models.IntegerField()
    premade_map_image = models.ImageField(null=True, upload_to='maps')


class GameMap(models.Model):
    map_hash = models.JSONField(default=dict)
    map_n = models.IntegerField()
    map_m = models.IntegerField()
    map_image = models.ImageField(null=True, upload_to='maps')


class PlayerInLobby(models.Model):
    player_Plobby = models.OneToOneField(User, on_delete=models.CASCADE)
    score_Plobby = models.IntegerField(default=0)
    fortune_Plobby = models.IntegerField(default=1000)
    returned_sync_Plobby = models.IntegerField(default=-1)
    epoch_sync_num_plobby = models.IntegerField(default=-1)

    def in_sync(self):
        return self.epoch_sync_num_plobby == self.returned_sync_Plobby


class Lobby(models.Model):
    player_1_lobby = models.OneToOneField(PlayerInLobby,
        related_name='+', on_delete=models.CASCADE)
    player_2_lobby = models.OneToOneField(PlayerInLobby,
        related_name='+', null=True, blank=True, on_delete=models.CASCADE)

    map_layout = models.ForeignKey(GameMap, on_delete=models.CASCADE)

    last_move_player = models.OneToOneField(PlayerInLobby, related_name='+',
                            default=None, null=True, on_delete=models.DO_NOTHING)

    last_move_i = models.IntegerField(null=True)
    last_move_j = models.IntegerField(null=True)
    last_move_act = models.IntegerField(choices=(
        (0, 'NULL'), (1, 'up'), (2, 'right'), (3, 'down'), (4, 'left'),), null=True)

    def delete(self, using=None, keep_parents=False):
        try:
            self.player_1_lobby.delete()
            self.map_layout.delete()
            self.player_2_lobby.delete()
        except: pass
        return super(Lobby, self).delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        try:
            if self.player_1_lobby.player_Plobby == self.player_2_lobby.player_Plobby:
                self.player_2_lobby.player_Plobby = None
        except: pass

        super(Lobby, self).save(force_insert,force_update,using,update_fields)
