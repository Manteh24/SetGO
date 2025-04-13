from django.db.models.signals import post_save
from django.dispatch import receiver
from gamification.models import PlayerProfile, Level
from accounts.models import Trainee  

@receiver(post_save, sender=Trainee)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'profile'):
            default_level = Level.objects.order_by('number').first()
            if not default_level:
                raise ValueError("No Level defined. Cannot create PlayerProfile.")
            PlayerProfile.objects.create(trainee=instance, level=default_level)
