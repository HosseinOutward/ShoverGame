from .views import LobbyAPIView, LobbyStatusAPIView, JoinLobby, LeaveLobby
from django.urls import path

urlpatterns = [
    path('_api/lobbies/', LobbyAPIView.as_view()),
    path('_api/GameLobby/', LobbyStatusAPIView.as_view()),
    path('_api/JoinLobby/<int:pk>', JoinLobby.as_view()),
    path('_api/LeaveLobby/', LeaveLobby.as_view()),
]
