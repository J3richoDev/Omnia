from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('members/create/', views.create_member, name='create_member'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('members/', views.members_list, name='members_list'),

    # newly added path
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password')
    # path('reset-password/', reset_password, name='reset_password')
]
