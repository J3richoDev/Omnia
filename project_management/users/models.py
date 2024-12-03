from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_first_login = models.BooleanField(default=True)

    # Defining roles with choices for 'Member' and 'Manager'
    MEMBER = 'member'
    MANAGER = 'manager'
    ROLE_CHOICES = [
        (MEMBER, 'Member'),
        (MANAGER, 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    # Profile picture that users can upload (optional field)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Optionally, you can override the save method to handle the `is_first_login` logic, if necessary:
    # def save(self, *args, **kwargs):
    #     if self.is_first_login:
    #         # handle first login logic
    #         pass
    #     super().save(*args, **kwargs)
