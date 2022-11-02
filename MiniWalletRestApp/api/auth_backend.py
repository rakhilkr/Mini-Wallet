from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class PasswordlessAuthBackend(BaseBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, request, username=None, password=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None