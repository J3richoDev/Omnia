from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Project

def validate_profile_picture(file):
    max_size = 2 * 1024 * 1024
    valid_extensions = ['.jpg', '.jpeg', '.png']

    if file.size > max_size:
        raise ValidationError('Profile picture file size cannot exceed 2 MB.')
    if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError('Invalid file format. Please upload a JPG, JPEG, or PNG file.')

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
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        validators=[validate_profile_picture]
    )
    assigned_projects = models.ManyToManyField(Project, related_name='members')

