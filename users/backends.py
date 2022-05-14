from django.contrib.auth.backends import ModelBackend
from users.models import User


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address Or Username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            if "@" in username:
                kwargs = {"email": username}
            else:
                kwargs = {"username": username}

        if password is None:
            return None
        try:
            user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
