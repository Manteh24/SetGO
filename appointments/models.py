from django.db import models
from accounts.models import Trainee, Trainer

class AppointmentRequest(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='appointment_requests')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='appointment_requests')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.trainee} requests {self.date} {self.start_time}-{self.end_time}"