from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MapLayout)
admin.site.register(Lobby)
admin.site.register(GameMap)
admin.site.register(PlayerInLobby)