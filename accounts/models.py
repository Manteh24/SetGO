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

    DAYS_OF_WEEK = (
        ('MO', 'Monday'),
        ('TU', 'Tuesday'),
        ('WE', 'Wednesday'),
        ('TH', 'Thursday'),
        ('FR', 'Friday'),
        ('SA', 'Saturday'),
        ('SU', 'Sunday'),
    )

    fixed_session_days = MultiSelectField(
        choices=DAYS_OF_WEEK,
        max_choices=7,
        max_length=20,
        blank=True
    )

    def __str__(self):
        return get_full_name_plus_username(self.user)
