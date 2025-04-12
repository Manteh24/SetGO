import math
from django.db import models
from accounts.models import Trainee


class PlayerProfile(models.Model):
    trainee = models.OneToOneField('accounts.Trainee', on_delete=models.CASCADE, related_name='profile')
    current_xp = models.PositiveIntegerField(default=0)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, blank=True)


class Level(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    xp_threshold = models.PositiveIntegerField()


    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Level {self.number}: {self.name}"
    

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon =  models.ImageField(upload_to='badges/')

    # conditions for earning the badge
    level_required = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    xp_required = models.PositiveIntegerField(null=True, blank=True)
    specific_task_count = models.PositiveIntegerField(null=True, blank=True)
    days_active_required = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class PlayerBadge(models.Model):
    profile = models.ForeignKey('PlayerProfile', on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE, related_name='awarded_to')
    date_awarded = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'badge')


    def __str__(self):
        return f"{self.profile.Trainee.user_name} - {self.badge.name}"