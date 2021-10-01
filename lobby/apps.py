from django.apps import AppConfig


class LobbyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lobby'

    def ready(self):
        import lobby.signals