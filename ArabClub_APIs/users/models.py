import re

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, username, date_of_birth, password):
        """
        Create and save a User with the given email and username, password.
        """

        if not email:
            raise ValueError(_('The Email must be set.'))

        is_valid_username = re.search(
            r'^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$',
            username
        )
        if not is_valid_username:
            raise ValueError(_('Enter Valid Username'))

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
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=50,
                                unique=True)
    date_of_birth = models.DateField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin


class FirstNameAndLastName(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Bio(models.Model):
    bio = models.TextField(max_length=255, verbose_name='Bio')
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.bio


class Phone(models.Model):
    phone = models.CharField(max_length=15, verbose_name='Phone Number')
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.phone


class GitHubAccount(models.Model):
    url = models.URLField()
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Skills(models.Model):
    skill_name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill_name


class Address(models.Model):
    country = models.CharField(max_length=50, verbose_name='Country')
    city = models.CharField(max_length=50, verbose_name='City')
    street_name = models.CharField(max_length=150, verbose_name='Street Name')
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.country

    @property
    def get_full_address(self):
        return f'{self.street_name}, {self.city}, {self.country}'

    @property
    def get_country(self):
        return self.country

    @property
    def get_city(self):
        return self.city

    @property
    def get_street(self):
        return self.street_name
