from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('members/create/', views.create_member, name='create_member'),
    path('get-member-projects/<int:member_id>/', views.get_member_projects, name='get_member_projects'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('members/', views.members_list, name='members_list'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('delete-user/', views.delete_user, name='delete_user'),

    # newly added path
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password')
    # path('reset-password/', reset_password, name='reset_password')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
