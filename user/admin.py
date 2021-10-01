from django.contrib import admin
from .models import UserProfile, ScoreBoardEntry


admin.site.register(ScoreBoardEntry)
admin.site.register(UserProfile)