from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Project(models.Model):
    COLOR_CHOICES = [
        ('purple', 'Purple'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('teal', 'Teal'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('pink', 'Pink'),
        ('gray', 'Grey'),
    ]
    name = models.CharField(max_length=100)
    emoji_icon = models.CharField(max_length=255, default='fa-star')
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue')
    current_sprint = models.ForeignKey('Sprint', on_delete=models.CASCADE, related_name='current_sprint', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.project.name}'

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks', blank=True)

    def __str__(self):
        return self.name

class TaskFile(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='task_files/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf', 'zip'])],
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"

class TaskComment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.name}"