import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from logging_manager import eventslog

# from newsfeed.models import Tag
logger = eventslog.logger


class CustomUserManager(BaseUserManager):
    """
    Custom user serializer manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, username, date_of_birth, password):
        """
        Create and save a User with the given email and username, password.
        """

        if not email:
            logger.error(_("The Email must be set."))
            raise ValueError(_("The Email must be set."))

        pattern = re.compile(
            r"^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        )
        if not re.fullmatch(pattern, username):
            logger.error(_("Enter Valid Username"))
            raise ValueError(_("Enter Valid Username"))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_of_birth, password):

        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email", max_length=255, unique=True
    )
    username = models.CharField(
        verbose_name="Username", max_length=50, unique=True
    )
    date_of_birth = models.DateField()
    join_date = models.DateTimeField(auto_now=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "date_of_birth"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin
