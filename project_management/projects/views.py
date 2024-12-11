from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import timedelta, datetime
from .models import Project, Task, TaskFile, TaskComment, ProjectMember, Sprint
from .forms import ProjectForm, TaskForm, TaskCommentForm, TaskFileForm, AddMemberForm, SprintForm

@login_required
def initial_setup(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            # Mark user as no longer first-time login
            request.user.is_first_login = False
            request.user.save()
            messages.success(request, "Project created successfully!" ,extra_tags="alert-success")
            return redirect('dashboard')  # Replace with your dashboard URL
        else:
            messages.error(request, "Failed to create the project. Please check the form and try again." ,extra_tags="alert-error")
    else:
        form = ProjectForm()
    icons = ['fa-star', 'fa-heart', 'fa-bell', 'fa-plus-square', 'fa-cog', 'fa-user', 'fa-pencil-alt', 'fa-building', 'fa-envelope', 'fa-search',
             'fa-camera', 'fa-laptop', 'fa-dollar', 'fa-shopping-cart', 'fa-download', 'fa-upload', 'fa-university', 'fa-comments', 'fa-users',
             'fa-thumbs-up', 'fa-gamepad', 'fa-home', 'fa-calendar', 'fa-clock', 'fa-wrench', 'fa-flag', 'fa-list', 'fa-folder',
             'fa-bookmark', 'fa-link', 'fa-map-marker-alt', 'fa-clipboard', 'fa-ticket', 'fa-bicycle', 'fa-car', 'fa-cogs',
             'fa-database', 'fa-paint-brush', 'fa-key', 'fa-gift', 'fa-cloud', 'fa-cloud-upload-alt', 'fa-file', 'fa-file-alt',
             'fa-comments', 'fa-briefcase', 'fa-legal', 'fa-paper-plane', 'fa-bolt', 'fa-lightbulb', 'fa-shield-alt']

    return render(request, 'projects/initial_project.html', {'form': form, 'icons': icons})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, "Project created successfully!" ,extra_tags="alert-success")
            return redirect('dashboard')  # Replace with your dashboard URL
        else:
            messages.error(request, "Failed to create the project. Please check the form and try again." ,extra_tags="alert-error")

    else:
        form = ProjectForm()
    icons = ['fa-star', 'fa-heart', 'fa-bell', 'fa-check', 'fa-cog', 'fa-user', 'fa-pencil-alt', 'fa-trash', 'fa-envelope', 'fa-search',
             'fa-plus', 'fa-minus', 'fa-cogs', 'fa-tasks', 'fa-download', 'fa-upload', 'fa-share', 'fa-comments', 'fa-users',
             'fa-thumbs-up', 'fa-cog', 'fa-home', 'fa-calendar', 'fa-clock', 'fa-wrench', 'fa-flag', 'fa-list', 'fa-folder',
             'fa-bookmark', 'fa-link', 'fa-map-marker-alt', 'fa-clipboard', 'fa-braille', 'fa-bicycle', 'fa-car', 'fa-cogs',
             'fa-database', 'fa-paint-brush', 'fa-key', 'fa-gift', 'fa-cloud', 'fa-cloud-upload-alt', 'fa-file', 'fa-file-alt',
             'fa-comments', 'fa-briefcase', 'fa-cogs', 'fa-paper-plane', 'fa-bolt', 'fa-lightbulb', 'fa-shield-alt']

    return render(request, 'projects/dashboard.html', {'form': form, 'icons': icons})

@csrf_exempt
def edit_project(request):
    if request.method == "POST":
        project_id = request.POST.get('project_id')
        name = request.POST.get('project_name')
        description = request.POST.get('description')
        color = request.POST.get('color')
        emoji_icon = request.POST.get('emoji_icon')

        try:
            project = Project.objects.get(id=project_id)
            project.name = name
            project.description = description
            project.color = color
            project.emoji_icon = emoji_icon
            project.save()

            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})



@login_required
def set_current_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id, owner=request.user)
        request.session['current_project_id'] = project.id
    except Project.DoesNotExist:
        messages.error(request, "The selected project does not exist or you do not have access." ,extra_tags="alert-error")
    return redirect('dashboard')

@login_required
def add_member(request):
    current_project_id = request.session.get('current_project_id')

    if not current_project_id:
        messages.warning(request, "No project selected. Please select a project first." ,extra_tags="alert-warning")
        return redirect('home')

    try:
        project = Project.objects.get(id=current_project_id)
    except Project.DoesNotExist:
        messages.error(request, "The project does not exist or you do not have access." ,extra_tags="alert-error")
        return redirect('home')

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            ProjectMember.objects.create(project=project, user=member)
            messages.success(request, f"Member {member.username} added to the project!" ,extra_tags="alert-success")
            return redirect('projects:create_task')  # Adjust as needed
        else:
            messages.error(request, "Failed to add member. Please check the form and try again." ,extra_tags="alert-error")
    else:
        form = AddMemberForm()

    return render(request, 'projects/add_member.html', {'form': form, 'project': project})

@login_required
def dashboard(request):
    user_projects = Project.objects.filter(owner=request.user) if request.user.role == 'manager' else []
    return render(request, 'projects/dashboard.html', {'projects': user_projects})

@login_required
def project_list(request):
    user_projects = Project.objects.filter(owner=request.user) if request.user.role == 'manager' else []
    return render(request, 'projects/project_list.html', {'projects': user_projects})

@login_required
def project_tasks(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    project = Project.objects.get(id=project_id, owner=request.user)
    tasks = project.tasks.all()

    return render(request, 'projects/project_tasks.html', {'tasks': tasks, 'project': project})

@login_required
def create_task(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        messages.warning(request, "No project selected. Please select a project first." ,extra_tags="alert-warning")
        return HttpResponseForbidden("No project selected.")

    try:
        project = Project.objects.get(id=project_id, owner=request.user)
    except Project.DoesNotExist:
        messages.error(request, "The project does not exist or you do not have access." ,extra_tags="alert-error")
        return HttpResponseForbidden("No project selected.")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            try:
                form.save_m2m()
                messages.success(request, f"Task '{task.name}' created successfully!" ,extra_tags="alert-success")
            except Exception as e:
                messages.error(request, f"Failed to save task relationships: {str(e)}" ,extra_tags="alert-error")
            return redirect('dashboard')  # Adjust as needed
        else:
            messages.error(request, "Failed to create the task. Please check the form and try again." ,extra_tags="alert-error")
    else:
        form = TaskForm()

    return render(request, 'projects/create_task.html', {'form': form, 'project': project})

@csrf_exempt
@login_required
@require_POST
def update_task_field(request):
    try:
        data = json.loads(request.body)
        task_id = data.get("task_id")
        field = data.get("field")
        value = data.get("value")

        task = Task.objects.get(id=task_id)

        # Ensure the field exists on the model
        if not hasattr(task, field):
            return JsonResponse({'success': False, 'error': 'Invalid field'})

        # Set the field value and save
        setattr(task, field, value)
        task.save()

        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def move_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        sprint_id = request.POST.get('sprint_id')

        try:
            task = Task.objects.get(id=task_id)
            if sprint_id == "backlog":
                task.sprint = None  # Move to backlog
            else:
                sprint = Sprint.objects.get(id=sprint_id)
                task.sprint = sprint

            task.save()
            return JsonResponse({'success': True})
        except (Task.DoesNotExist, Sprint.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Task or Sprint not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def my_tasks(request):
    if request.user.role != 'member':
        return redirect('dashboard')  # Redirect non-members to the dashboard

    tasks = Task.objects.filter(assigned_members=request.user)
    context = {'tasks': tasks}
    return render(request, 'projects/my_tasks.html', context)

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    comments = task.comments.all()
    files = task.files.all()

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_form = TaskCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.author = request.user
                comment.save()
                return redirect('task_detail', task_id=task_id)

        if 'file' in request.FILES:
            file_form = TaskFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                task_file = file_form.save(commit=False)
                task_file.task = task
                task_file.uploaded_by = request.user
                task_file.save()
                return redirect('task_detail', task_id=task_id)
    else:
        comment_form = TaskCommentForm()
        file_form = TaskFileForm()

    return render(
        request,
        'projects/task_detail.html',
        {
            'task': task,
            'comments': comments,
            'files': files,
            'comment_form': comment_form,
            'file_form': file_form,
        },
    )

@login_required
def delete_file(request, file_id):
    task_file = TaskFile.objects.get(id=file_id)
    if request.user == task_file.task.project.owner:
        task_file.delete()
    return redirect('task_detail', task_id=task_file.task.id)

@login_required
def project_sprints(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    today = now().date()
    project = Project.objects.get(id=project_id, owner=request.user)
    sprints = project.sprints.all().order_by('start_date')
    active_sprints = project.sprints.filter(ended=False).order_by('start_date')
    sprint_count = sprints.count()
    backlog_tasks = project.tasks.filter(sprint__isnull=True)
    sprints_with_tasks = {
        sprint: sprint.tasks.all() for sprint in active_sprints
    }

    existing_start_dates = [sprint.start_date.strftime('%Y-%m-%d') for sprint in sprints]

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, "Sprint created successfully!", extra_tags="alert-success")
            return redirect('project_sprints')
        else:
            messages.error(request, "Failed to create the sprint. Please check the form and try again.", extra_tags="alert-error")
    else:
        form = SprintForm()

    return render(request, 'projects/project_sprints.html', {
        'today':today,
        'existing_start_dates': json.dumps(existing_start_dates),
        'sprints_with_tasks': sprints_with_tasks,
        'sprint_count' : sprint_count,
        'available_sprints': sprints,
        'backlog_tasks': backlog_tasks,
        'project': project,
        'form': form
    })

@csrf_exempt
@login_required
def create_sprint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = request.session.get('current_project_id')
            project = Project.objects.get(id=project_id)

            # Calculate end date if duration is specified
            if data['duration'] != 'custom':
                start_date = data['start_date']
                duration = int(data['duration']) * 7  # Convert weeks to days
                end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=duration - 1)).date()
            else:
                end_date = data['end_date']

            Sprint.objects.create(
                project=project,
                name=data['name'],
                start_date=data['start_date'],
                end_date=end_date,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def validate_start_date(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            # Check if a sprint already exists with the same start date
            exists = Sprint.objects.filter(start_date=start_date).exists()
            return JsonResponse({'exists': exists})
        else:
            return JsonResponse({'exists': False})


def start_sprint(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project

    if project.current_sprint:
        messages.error(request, "You must end the current sprint before starting a new one.")
        return redirect('project_sprints')

    sprint.is_active = True
    project.current_sprint = sprint
    sprint.save()
    project.save()

    messages.success(request, f"Sprint '{sprint.name}' started successfully!")
    return redirect('project_sprints')

def end_sprint(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project

    if project.current_sprint != sprint:
        messages.error(request, "This sprint is not currently active.")
        return redirect('project_sprints')

    sprint.is_active = False
    sprint.ended = True
    project.current_sprint = None
    sprint.save()
    project.save()

    messages.success(request, f"'{sprint.name}' ended successfully!")
    return redirect('project_sprints')

@csrf_exempt
@login_required
def update_task_sprint(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_sprint_id = request.POST.get('new_sprint_id')

        try:
            task = Task.objects.get(id=task_id)
            if new_sprint_id:
                task.sprint_id = new_sprint_id
            else:
                task.sprint = None  # Move to backlog
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def edit_sprint(request):
    if request.method == 'POST':
        sprint_id = request.POST.get('sprint_id')
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            sprint = Sprint.objects.get(id=sprint_id)
            sprint.name = name
            sprint.start_date = start_date
            sprint.end_date = end_date
            sprint.save()
            return JsonResponse({'success': True})
        except Sprint.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sprint not found'})

@login_required
def delete_sprint(request):
    if request.method == 'POST':
        sprint_id = request.POST.get('sprint_id')

        try:
            sprint = Sprint.objects.get(id=sprint_id)

            tasks = Task.objects.filter(sprint=sprint)
            tasks.update(sprint=None)

            sprint.delete()

            return JsonResponse({'success': True})
        except Sprint.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sprint not found'})

@login_required
def kanban_board(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    project = Project.objects.get(id=project_id)

    # Ensure we only fetch tasks for the current active sprint
    current_sprint = project.current_sprint
    if current_sprint:
        tasks = current_sprint.tasks.all()
        tasks_by_status = {
            'todo': tasks.filter(status='todo'),
            'in_progress': tasks.filter(status='in_progress'),
            'review': tasks.filter(status='review'),
            'completed': tasks.filter(status='completed'),
        }
    else:
        tasks_by_status = {}  # No tasks if there is no active sprint

    return render(request, 'projects/kanban_board.html', {
        'project': project,
        'tasks_by_status': tasks_by_status,
        'current_sprint': current_sprint,
    })

@login_required
def my_kanban_board(request):
    if request.user.role != 'member':
        return redirect('dashboard')  # Redirect non-members to the dashboard

    tasks = Task.objects.filter(assigned_members=request.user)
    if tasks.exists():
        project = tasks.first().project
    else:
        project = None
    tasks_by_status = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'review': tasks.filter(status='review'),
        'completed': tasks.filter(status='completed'),
    }
    return render(request, 'projects/kanban_board.html', {'project': project, 'tasks_by_status': tasks_by_status})

@csrf_exempt
@login_required
def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('new_status')
        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def gantt_chart(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    project = Project.objects.get(id=project_id, owner=request.user)
    tasks = Task.objects.filter(project=project)

    # Prepare data for Gantt chart
    task_data = [
        {
            "id": task.id,
            "name": task.name,
            "start": task.start_date.isoformat(),
            "end": task.end_date.isoformat(),
            "status": task.status,
            "priority": task.priority,
            "description": task.description,
        }
        for task in tasks
    ]

    context = {
        "project": project,
        "tasks_json": task_data,
    }
    return render(request, "projects/gantt_chart.html", context)

@login_required
def project_members(request):
    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    project = Project.objects.get(id=project_id, owner=request.user)
    return render(request, 'projects/members.html', {'project': project})

