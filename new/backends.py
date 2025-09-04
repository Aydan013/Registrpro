from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomerUser = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomerUser.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
        except CustomerUser.DoesNotExist:
            return None
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return CustomerUser.objects.get(pk=user_id)
        except CustomerUser.DoesNotExist:
            return None