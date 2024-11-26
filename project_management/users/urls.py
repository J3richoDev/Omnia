from django.urls import path
from .views import register
from .views import create_member
from .views import complete_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('members/create/', create_member, name='create_member'),
    path('complete-profile/', complete_profile, name='complete_profile'),
]
