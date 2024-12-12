from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, MemberCreationForm, MemberProfileForm, UserUpdateForm, PasswordChangeForm, CustomAuthenticationForm
from .models import CustomUser
from django.shortcuts import render, get_object_or_404
from projects.models import Project, ProjectMember  # Replace `your_app` with the correct app name

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = request.POST.get('password')

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

    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace with your login URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
@login_required
def create_member(request):
    if request.user.role != CustomUser.MANAGER:
        return redirect('dashboard')  # Restrict access to managers

    if request.method == 'POST':
        form = MemberCreationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.role = CustomUser.MEMBER
            member.set_password(form.cleaned_data['password'])
            project = get_object_or_404(Project, id=request.POST.get('project_id')) 
            try:
                member.save()
                ProjectMember.objects.create(project=project, user=member)
                messages.success(request, "Member created successfully!", extra_tags="alert-success")
                return redirect('create_member')  # Replace with your members list URL
            except IntegrityError:
                messages.error(request, "A user with this email already exists.", extra_tags="alert-error")
        else:
            messages.error(request, "Failed to create the member. Please check the form and try again.", extra_tags="alert-error")
    else:
        form = MemberCreationForm()

    members = CustomUser.objects.filter(role=CustomUser.MEMBER)
    return render(request, 'users/create_member.html', {'form': form, 'members': members})





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

    # Initialize the forms with the user's data
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm()
    context = {
        "user_form": user_form,
        "password_form": password_form,
    }

    if request.method == "POST":
        if "save_profile" in request.POST:
            # Handle profile picture update
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect("my_profile")

        elif "update_info" in request.POST:
            # Handle general user info update
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Info changed successfully!")
                return redirect("my_profile")

        elif "change_password" in request.POST:
            # Handle password change
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data["old_password"]
                new_password = password_form.cleaned_data["new_password"]

                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully!")
                    update_session_auth_hash(request, user)  # Keep user logged in
                    return redirect("my_profile")
                else:
                    password_form.add_error("old_password", "Old password is incorrect.")

    context["user_form"] = user_form
    context["password_form"] = password_form
    return render(request, "users/my_profile.html", context)

@login_required
def members_list(request):
    members = CustomUser.objects.filter(role=CustomUser.MEMBER)  # Fetch members with a specific role
    return render(request, 'users/members_list.html', {'members': members})




def logout_view(request):
    logout(request)
    return redirect('login')



