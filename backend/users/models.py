from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Aap yahan aur bhi fields add kar sakte hain, jaise bio, location, etc.
    # Abhi ke liye, yeh structure kaafi hai.

    def __str__(self):
        return f'{self.user.username} Profile'