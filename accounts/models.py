from django.db import models
from django.contrib.auth.models import User
from .handy_tools import get_full_name_plus_username
from multiselectfield import MultiSelectField


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    message_to_trainees = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return get_full_name_plus_username(self.user)


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name='trainees')

    def __str__(self):
        return get_full_name_plus_username(self.user)


class FixedSession(models.Model):
    DAY_CHOICES = [
        ('SA', 'Saturday'),
        ('SU', 'Sunday'),
        ('MO', 'Monday'),
        ('TU', 'Tuesday'),
        ('WE', 'Wednesday'),
        ('TH', 'Thursday'),
        ('FR', 'Friday'),
    ]

    trainee = models.ForeignKey("Trainee", on_delete=models.CASCADE, related_name='fixed_sessions')
    day_of_week = models.CharField(max_length=2, choices=DAY_CHOICES)
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.trainee} - {self.day_of_week} {self.start_time}-{self.end_time}"