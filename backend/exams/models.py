
# Create your models here.

from django.db import models
from django.contrib.auth.models import User # User model ko import karein

class ExamCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    logo_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        # Admin panel mein iska naam theek se dikhane ke liye
        verbose_name_plural = "Exam Categories"


class Exam(models.Model):
    # Har exam ko ek category se jodein
    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, related_name='exams', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    logo_url = models.URLField(max_length=200, blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_exams', blank=True)

    def __str__(self):
        return self.title
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10,null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) # Message kab aaya, woh time automatically save hoga
    is_read = models.BooleanField(default=False) # Admin ne message padha ya nahi

    def __str__(self):
        return f"Message from {self.name} ({self.email})"    