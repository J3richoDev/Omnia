from django.urls import path
from .views import create_project
from . import views

urlpatterns = [
    path('create/', create_project, name='create_project'),
<<<<<<< Updated upstream
    path('reports/', views.reports_view, name='reports'),
=======
>>>>>>> Stashed changes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('set_project/<int:project_id>/', views.set_current_project, name='set_current_project'),
    path('tasks/', views.project_tasks, name='project_tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('my-kanban/', views.my_kanban_board, name='my_kanban'),
    path('tasks/update_status/', views.update_task_status, name='update_task_status'),
    path('gantt/', views.gantt_chart, name='gantt_chart'),
]
