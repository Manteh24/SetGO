from datetime import date
from django.db import models
from accounts.models import Trainer, Trainee


class Task(models.Model):
    DRILL_TYPES = [
        ('warmup', 'Warm-Up & Movement'),
        ('groundstroke', 'Groundstroke Drill'),
        ('target', 'Target Drill'),
        ('power', 'Power & Consistency'),
        ('serve', 'Serve Drill'),
        ('tactical', 'Tactical/Pattern Drill'),
        ('fitness', 'Fitness Drill'),
        ('situational', 'Situational Drill'),
        ('solo', 'Solo/Wall Drill'),
        ('custom', 'Custom Drill'),
    ]
        
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='tasks') 
    xp_reward = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=50, choices=DRILL_TYPES)

    def __str__(self):
        return self.title
    

class TaskAssignment(models.Model):
    trainee = models.ForeignKey(Trainee , on_delete=models.CASCADE, related_name='tasks_assigned')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    @property
    def days_remaining(self):
        remaining_days = (self.due_date - date.today()).days
        return max(remaining_days, 0)
    
    def __str__(self):
        return f"{self.task.title} for {self.trainee.user.username} (Due: {self.due_date})"