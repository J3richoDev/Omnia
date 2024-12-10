from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_first_login = models.BooleanField(default=True)
    MEMBER = 'member'
    MANAGER = 'manager'
    ROLE_CHOICES = [
        (MEMBER, 'Member'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MANAGER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # other fields...

    def __str__(self):
        return self.name