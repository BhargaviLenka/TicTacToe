from django.contrib import admin
from .models import Game, Player, Leaderboard

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Leaderboard)

