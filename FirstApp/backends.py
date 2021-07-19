from .models import *
from django.conf import settings

class AuthBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Register.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Register.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return Register.objects.get(pk=user_id)
        except Register.DoesNotExist:
            return None
