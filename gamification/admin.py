from django.contrib import admin
from gamification.models import PlayerProfile, Level, Badge, PlayerBadge


admin.site.register(PlayerProfile)
admin.site.register(Level)
admin.site.register(Badge)
admin.site.register(PlayerBadge)
