from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import *


def get_current_player(lobby, user):
    player = lobby.player_1_lobby
    other_player = lobby.player_2_lobby
    if player.player_Plobby != user:
        player = lobby.player_2_lobby
        other_player = lobby.player_1_lobby
    return player, other_player


class LobbySerializer(serializers.ModelSerializer):
    map_choice = serializers.PrimaryKeyRelatedField(queryset=MapLayout.objects.all())

    class Meta:
        model = Lobby
        fields = ["map_choice"]

    def create(self, validated_data):
        try:
            current_lobby = Lobby.objects.filter(player_1_lobby=self.context['request'].user.playerinlobby).get()
            current_lobby.delete()
        except: pass
        player_1_lobby = PlayerInLobby(player_Plobby=self.context['request'].user)
        map_choice = validated_data['map_choice']
        map_layout = GameMap(map_hash=map_choice.premade_map_hash,
            map_n=map_choice.premade_map_n, map_m=map_choice.premade_map_m,
            map_image=map_choice.premade_map_image)

        del validated_data['map_choice']

        try:
            player_1_lobby.save()
            map_layout.save()
            validated_data['map_layout'] = map_layout
            validated_data['player_1_lobby'] = player_1_lobby
        except:
            try:
                player_1_lobby.delete()
                map_layout.delete()
            except: raise PermissionDenied(
                {"message":"something went wrong during saving player or map data"})
        return super().create(validated_data)


class GetLobbySerializer(serializers.ModelSerializer):
    player1 = serializers.CharField(source="player_1_lobby.player_Plobby")
    player2 = serializers.CharField(source="player_2_lobby.player_Plobby", allow_null=True)
    map_image = serializers.CharField(source="map_layout.map_image", allow_null=True)

    class Meta:
        model = Lobby
        fields = ['pk', "player1", "player2", "map_image"]
        read_only_fields = fields


class JoinLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = []

    def update(self, instance, validated_data):
        user = self.context['request'].user
        obj_querylist = PlayerInLobby.objects.filter(player_Plobby=user)
        if obj_querylist: raise PermissionDenied({"message":"cant join"})
        player_2_lobby = PlayerInLobby(player_Plobby=user)
        player_2_lobby.save()
        validated_data['player_2_lobby'] = player_2_lobby
        return super().update(instance, validated_data)


class LeaveLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = []

    def update(self, instance, validated_data):
        instance.delete()
        return super().update(instance, validated_data)


class GameStatusSerializers(serializers.ModelSerializer):
    my_turn = serializers.SerializerMethodField()
    synced = serializers.SerializerMethodField()
    epoch_num = serializers.SerializerMethodField()
    turn_switch = serializers.SerializerMethodField()
    players_info = serializers.SerializerMethodField()

    class Meta:
        model = Lobby
        fields = ['id', 'my_turn', "synced", 'epoch_num', 'players_info', 'turn_switch',
                  "last_move_i", "last_move_j", "last_move_act", "map_layout"]
        depth=1

    def update(self, instance, validated_data):
        if validated_data.get('last_move_i') or \
                validated_data.get('last_move_j') or validated_data.get('last_move_act'):
            p1 = instance.player_1_lobby
            p2 = instance.player_2_lobby
            p1.epoch_sync_num_plobby += 1
            p2.epoch_sync_num_plobby += 1
            p1.save(); p2.save()

            player, _ = get_current_player(instance, self.context['request'].user)
            instance.last_move_player = player
            instance.save()

        return super().update(instance, validated_data)

    def get_my_turn(self, obj):
        player, other_player = get_current_player(obj, self.context['request'].user)
        is_host = (player == obj.player_1_lobby)

        if other_player is None: return False

        if player.fortune_Plobby == other_player.fortune_Plobby: result = not is_host
        else: result = player.fortune_Plobby > other_player.fortune_Plobby

        return result

    def get_synced(self, obj):
        player, other_player = get_current_player(obj, self.context['request'].user)
        try: return (player.in_sync() and other_player.in_sync())
        except: return False

    def get_players_info(self, obj):
        from PIL import ImageColor
        player, other_player = get_current_player(obj, self.context['request'].user)
        is_host = (player == obj.player_1_lobby)

        player = {
            'score_Plobby': player.score_Plobby,
            'fortune_Plobby': player.fortune_Plobby,
            'color': ImageColor.getcolor(
                player.player_Plobby.userprofile.color_profile, "RGB"),
            'color_map_code': int(is_host)
        }
        if other_player is not None:
            other_player = {
                'score_Plobby': other_player.score_Plobby,
                'fortune_Plobby': other_player.fortune_Plobby,
                'color': ImageColor.getcolor(
                    other_player.player_Plobby.userprofile.color_profile, "RGB"),
                'color_map_code': int(is_host)
            }
        else: other_player = ""

        return {'player': player, 'other_player': other_player}

    def get_epoch_num(self, obj):
        player, _ = get_current_player(obj, self.context['request'].user)
        return player.epoch_sync_num_plobby

    def get_turn_switch(self, obj):
        player, other_player = get_current_player(obj, self.context['request'].user)
        my_turn=self.get_my_turn(obj)

        if not self.get_synced(obj): return 0
        if obj.last_move_player != player and my_turn: return 1
        elif obj.last_move_player != other_player and not my_turn: return 2


class PlayerStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlayerInLobby
        fields = '__all__'


