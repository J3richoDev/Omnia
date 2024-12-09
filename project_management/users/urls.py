
from django.urls import path
from .views import register, logout_view, login_view
from .views import create_member
from .views import complete_profile, my_profile
from .views import forgot_password, reset_password


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('members/create/', create_member, name='create_member'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('my-profile/', my_profile, name='my_profile'),

    #newly added path
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password')
    # path('reset-password/', reset_password, name='reset_password')

]
