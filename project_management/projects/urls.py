from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users.views import members_list

urlpatterns = [
    path('setup/', views.initial_setup, name='initial_setup'),
    path('create/', views.create_project, name='create_project'),
    path('dashboard/', views.dashboard, name='dashboard'),
    

    path('set_project/<int:project_id>/', views.set_current_project, name='set_current_project'),
    path('projects/', views.project_list, name='projects'),
    path('projects/edit', views.edit_project, name='edit_project'),

    path('members/', views.project_members, name='members'),
    path('add_member/', views.add_member, name='add_member'),

    path('tasks/', views.project_tasks, name='project_tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/update-field/', views.update_task_field, name='update_task_field'),
    path('delete-task/', views.delete_task, name='delete_task'),
    path('move-task/', views.move_task, name='move_task'),
    path('tasks/<int:task_id>/assign-members/', views.assign_members, name='assign_members'),
    path('tasks/update-detail/', views.update_task_detail, name='update_task_detail'),
    # path('tasks/update_task_sprint/', views.update_task_sprint, name='update_task_sprint'),

    path('sprints/', views.project_sprints, name='project_sprints'),
    path('sprints/create/', views.create_sprint, name='create_sprint'),
    path('validate_start_date/', views.validate_start_date, name='validate_start_date'),
    path('update-task-sprint/', views.update_task_sprint, name='update_task_sprint'),
    path('sprints/edit', views.edit_sprint, name='edit_sprint'),
    path('sprints/delete', views.delete_sprint, name='delete_sprint'),
    path('start-sprint/<int:sprint_id>/', views.start_sprint, name='start_sprint'),
    path('end-sprint/<int:sprint_id>/', views.end_sprint, name='end_sprint'),


    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('my_tasks/<int:task_id>/', views.my_task_detail, name='my_task_detail'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),

    path('my-sprints/', views.my_project_sprints, name='my_project_sprints'),
    path('update-bulk-task-status/', views.update_bulk_task_status, name='update_bulk_task_status'),

    path('kanban/', views.kanban_board, name='kanban_board'),
    path('my-kanban/', views.my_kanban_board, name='my_kanban'),
    path('tasks/update_status/', views.update_task_status, name='update_task_status'),

    path('gantt/', views.gantt_chart, name='gantt_chart'),
    path('reports/', views.reports_view, name='reports'),
    path('users/', include('users.urls')),

    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('notifications/read/<int:notification_id>/', views.read_and_redirect,name='read_and_redirect'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)