from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, MemberCreationForm, MemberProfileForm, UserUpdateForm, PasswordChangeForm, CustomAuthenticationForm
from .models import CustomUser
import logging

# Set up logging
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = request.POST.get('password')

            logger.debug(f"Attempting login with username/email: {username} and password: {password}")

            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def create_member(request):
    if request.user.role != CustomUser.MANAGER:
        return redirect('dashboard')

    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.role = CustomUser.MEMBER
            member.set_password(form.cleaned_data['password'])
            member.save()
            return redirect('members_list')
    else:
        form = MemberCreationForm()

    return render(request, 'users/create_member.html', {'form': form})

@login_required
def complete_profile(request):
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('dashboard')
    else:
        form = MemberProfileForm(instance=request.user)

    return render(request, 'users/complete_profile.html', {'form': form})

@login_required
def my_profile(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm(request.POST or None)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                user_form.save()

                # Log profile picture upload
                if 'profile_picture' in user_form.cleaned_data and user_form.cleaned_data['profile_picture']:
                    logger.info("Profile picture uploaded: %s", user_form.cleaned_data['profile_picture'])

                messages.success(request, "Profile picture updated successfully!")
                return redirect('my_profile')

        elif 'update_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Info updated successfully!")
                return redirect('my_profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.POST)

            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                new_password = password_form.cleaned_data['new_password']

                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully!")
                    update_session_auth_hash(request, user)
                    return redirect('my_profile')
                else:
                    password_form.add_error('old_password', "Old password is incorrect.")

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }

    return render(request, 'users/my_profile.html', context)



def logout_view(request):
    logout(request)
    logger.info("User logged out successfully.")
    return redirect('login')