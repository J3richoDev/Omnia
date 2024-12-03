from django.urls import path
from .views import login_view, logout_view  # Import your logout view
from django.contrib.auth import views as auth_views
from .views import register, create_member, complete_profile, my_profile, login_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('members/create/', create_member, name='create_member'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('my-profile/', my_profile, name='my_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

