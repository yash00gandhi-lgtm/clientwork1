from django.db import models
from leads.models import Lead


class Booking(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='bookings')

    program = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.name} - {self.program}"