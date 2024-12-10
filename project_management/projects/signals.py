from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Task
from django.contrib.auth.signals import user_logged_in
from .models import Project

<<<<<<< Updated upstream

=======
@receiver(m2m_changed, sender=Task.assigned_members.through)
def notify_members_on_assignment(sender, instance, action, **kwargs):
    if action == 'post_add':
        members = instance.assigned_members.all()
        for member in members:
            send_mail(
                subject=f"New Task Assigned: {instance.name}",
                message=f"You have been assigned to the task: {instance.name} in the project: {instance.project.name}.",
                from_email='noreply@projectmanagement.com',
                recipient_list=[member.email],
            )
>>>>>>> Stashed changes

@receiver(user_logged_in)
def set_current_project(sender, request, user, **kwargs):
    if user.role == 'manager':
        # Set the first project the manager created
        first_project = Project.objects.filter(owner=user).first()
        if first_project:
            request.session['current_project_id'] = first_project.id
    else:
        # Set the first project the member is involved in
        request.session['current_project_id'] = None
