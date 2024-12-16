from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages
from django.urls import reverse

from .forms import CustomUserCreationForm, MemberCreationForm, MemberProfileForm, UserUpdateForm, PasswordChangeForm, \
    CustomAuthenticationForm, ForgotPasswordForm, ResetPasswordForm, AssignProjectsForm
from .models import CustomUser
from projects.models import Project, ProjectMember, Notification
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))
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
def project_list(request):
    user_projects = Project.objects.filter(owner=request.user) if request.user.role == 'manager' else []
    return render(request, 'projects/project_list.html', {'projects': user_projects})


@login_required
def create_member(request):
    # Restrict access to project managers
    if request.user.role != CustomUser.MANAGER:
        return redirect('dashboard')

    project_id = request.session.get('current_project_id')
    if not project_id:
        return HttpResponseForbidden("No project selected.")

    # Retrieve the selected project
    try:
        project = get_object_or_404(Project, id=project_id, owner=request.user)
    except ValueError:
        messages.error(request, "Invalid project ID.", extra_tags="alert-error")
        return redirect('dashboard')

    member_form = MemberCreationForm()
    assign_form = AssignProjectsForm()

    if request.method == 'POST':
        # Handle Member Creation Form
        if 'btnform1' in request.POST:
            member_form = MemberCreationForm(request.POST, request.FILES)
            if member_form.is_valid():
                member = member_form.save(commit=False)
                member.role = CustomUser.MEMBER
                member.set_password(member_form.cleaned_data['password'])
                try:
                    member.save()
                    ProjectMember.objects.create(project=project, user=member)

                    Notification.objects.create(
                        user=member,
                        actor=request.user,
                        message=f"{request.user.get_full_name()} added you to the project '{project.name}'."
                    )


                    messages.success(request, "Member created successfully!", extra_tags="alert-success")
                    return redirect('create_member')
                except IntegrityError:
                    messages.error(request, "A user with this email already exists.", extra_tags="alert-error")
            else:
                messages.error(request, "Failed to create the member. Please check the form.", extra_tags="alert-error")

        # Handle Assign Projects Form
        elif 'btnform2' in request.POST:
            assign_form = AssignProjectsForm(request.POST)
            if assign_form.is_valid():
                user_id = request.POST.get('user_id')  # Retrieve user ID from the hidden input
                member = get_object_or_404(CustomUser, id=user_id)
                projects = assign_form.cleaned_data['assigned_projects']
                # Get the current assigned projects
                current_projects = set(member.assigned_projects.all())

                # Find newly added projects
                new_projects = set(projects) - current_projects

                # Update the assigned projects
                member.assigned_projects.set(projects)

                # Notify only for newly added projects
                for project in new_projects:
                    Notification.objects.create(
                        user=member,
                        actor=request.user,
                        message=f"{request.user.get_full_name()} has assigned you to the project '{project.name}'."
                    )

                messages.success(request, f"Projects assigned to {member.username} successfully!",
                                 extra_tags="alert-success")
                return redirect('create_member')
            else:
                messages.error(request, "Failed to assign projects. Please check the form.", extra_tags="alert-error")

    # Retrieve existing members for display
    members = CustomUser.objects.filter(role=CustomUser.MEMBER)
    user_projects = Project.objects.filter(owner=request.user) if request.user.role == 'manager' else []

    return render(request, 'users/create_member.html', {
        'member_form': member_form,
        'assign_form': assign_form,
        'members': members,
        'projects': user_projects,
    })

@login_required
def get_member_projects(request, member_id):
    # Ensure only managers can access this
    if request.user.role != CustomUser.MANAGER:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Fetch the member and their assigned projects
    member = get_object_or_404(CustomUser, id=member_id)
    assigned_projects = member.assigned_projects.values_list('id', flat=True)

    return JsonResponse({'assigned_projects': list(assigned_projects)})

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
def upload_photo(request):
    if request.method == "POST" and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        print("MEDIA_ROOT:", settings.MEDIA_ROOT)
        print("Saved file path:", user.profile_picture.path)
        print("File URL:", user.profile_picture.url)
        messages.success(request,"Profile Picture changed successfully!",extra_tags="alert-success")
        return JsonResponse({'new_photo_url': user.profile_picture.url})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Deletes the user
        logout(request)  # Logs out the user
        return JsonResponse({'success': True, 'message': 'Account deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def my_profile(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        is_user_form_valid = user_form.is_valid()
        password_attempt = any(request.POST.get(field) for field in ['old_password', 'new_password', 'confirm_password'])
        is_password_form_valid = password_form.is_valid() if password_attempt else False

        # Process password change if there's an attempt
        if password_attempt:
            if is_password_form_valid:
                new_password = password_form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in
                messages.success(request, "Password changed successfully!")
            else:
                messages.error(request, "Please correct the errors in the password form.")
                print("Password Form Errors:", password_form.errors)  # Debug errors

        # Both forms are valid and all updates are successful
        if is_user_form_valid and (not password_attempt or is_password_form_valid):
            if is_user_form_valid:  # Only save and show message if user form is valid
                user_form.save()
                messages.success(request, "Profile updated successfully!")
            return redirect("my_profile")

    context = {
        "user_form": user_form,
        "password_form": password_form,
    }
    return render(request, "users/my_profile.html", context)


@login_required
def members_list(request):
    members = CustomUser.objects.filter(role=CustomUser.MEMBER)
    return render(request, 'users/members_list.html', {'members': members})


def logout_view(request):
    logout(request)
    return redirect('login')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         if email:
#             try:
#                 user = CustomUser.objects.get(email=email)

#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(str(user.pk).encode())

#                 reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"

#                 send_mail(
#                     "Password Reset Request",
#                     f"Click the link to reset your password: {reset_url}",
#                     "no-reply@omnia.com",
#                     [email],
#                 )

#                 messages.success(request, "A password reset link has been sent to your email address.")
#                 return redirect('login')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, "No user found with that email address.")
#         else:
#             messages.error(request, "Please provide a valid email address.")

#     return render(request, 'users/forgotpass.html')
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                # Generate token and URL for password reset
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                # Generate the password reset URL
                reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"
                # Send email
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email="no-reply@omnia.com",  # Replace with your email address
                    recipient_list=[email],
                )
                messages.success(request, "A password reset link has been sent to your email address.")
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that email address.")
        else:
            messages.error(request, "Please provide a valid email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgotpass.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect('login')
        else:
            form = ResetPasswordForm(user)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {'form': form})
# def reset_password(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Your password has been reset successfully!")
#                 return redirect('login')
#         else:
#             form = SetPasswordForm(user)
#     else:
#         messages.error(request, "The reset link is invalid or has expired.")
#         return redirect('login')

#     return render(request, 'users/reset_password.html', {'form': form})

