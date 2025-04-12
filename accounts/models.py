from django.db import models
from django.contrib.auth.models import User
from .handy_tools import get_full_name_plus_username


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
