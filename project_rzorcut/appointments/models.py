from django.db import models
from django.contrib.auth.models import User
import random
import string
from datetime import time
# Create your models here.
from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    opening_time = models.TimeField(default=time(9, 0))  # e.g. 9 AM
    closing_time = models.TimeField(default=time(17, 0))  # e.g. 5 PM

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='appointments')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    appointment_time = models.DateTimeField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} @ {self.store.name} on {self.appointment_time}"

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.otp = generate_otp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.otp}"

