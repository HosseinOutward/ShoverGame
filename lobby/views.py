from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Lobby
from rest_framework.exceptions import PermissionDenied


class LobbyAPIView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lobby.objects.all()

    def get_serializer_class(self):
        serializer_class = LobbySerializer
        if self.request.method == 'LIST' or self.request.method == 'GET':
            serializer_class = GetLobbySerializer
        return serializer_class


class LobbyStatusAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GameStatusSerializers

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(player_1_lobby__player_Plobby=self.request.user)
        try: obj=obj.get()
        except: pass
        if not obj: obj = get_object_or_404(queryset, player_2_lobby__player_Plobby=self.request.user)
        return obj

    def get_queryset(self):
        return Lobby.objects.all()

    def update(self, request, *args, **kwargs):
        lobby = self.get_object()
        try:
            player, other_player = get_current_player(lobby, self.request.user)
        except: raise PermissionDenied({"message": "You don't have permission to edit this game"})

        try:
            if player.returned_sync_Plobby == request.POST["randomSynch_my"]\
                    and other_player.fortune_Plobby != request.POST["fortune_enemy"]:
                lobby.delete()
        except: pass

        try:
            player.returned_sync_Plobby = request.POST["epoch_num_my"]
            player.save()
            player.fortune_Plobby = request.POST["fortune_my"]
            player.score_Plobby = request.POST["score_my"]
            player.save()
        except: pass

        return super(LobbyStatusAPIView, self).update(request, *args, **kwargs)


class JoinLobby(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JoinLobbySerializer
    queryset = Lobby.objects.all()


class LeaveLobby(generics.DestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveLobbySerializer
    queryset = Lobby.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(player_1_lobby__player_Plobby=self.request.user)
        try: obj=obj.get()
        except: pass
        if not obj: obj = get_object_or_404(queryset, player_2_lobby__player_Plobby=self.request.user)
        return obj