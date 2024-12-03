from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to authenticate based on email first
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            try:
                # If email doesn't exist, try username
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return None  # Return None if no matching user is found

        if user.check_password(password):  # Check password
            return user
        return None  # Return None if the password is incorrect

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
