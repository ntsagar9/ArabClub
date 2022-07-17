from django.contrib.auth.backends import ModelBackend

from logging_manager import eventslog
from user.models import User


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address Or Username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger = eventslog.logger
        try:
            if username is not None:
                if "@" in username:
                    kwargs = {"email": username}
                else:
                    kwargs = {"username": username}

            if password is None:
                logger.error("Request with password is None!:", request.data)
                return None
            try:
                user = User.objects.get(**kwargs)
            except User.DoesNotExist:
                pass
            else:
                if user.check_password(
                    password
                ) and self.user_can_authenticate(user):
                    return user
        except Exception as e:
            logger.error(f"{e} - {request}")
