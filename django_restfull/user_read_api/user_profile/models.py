from django.db import models
from django.urls import reverse

"""
Create tables in database for more user information
with relationship with user
"""
from user.models import User


class Name(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    user = models.OneToOneField(
        User, related_name="name", primary_key=True, on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.first_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Bio(models.Model):
    bio = models.TextField(max_length=255, verbose_name="Bio")
    user = models.OneToOneField(
        User, related_name="bio", primary_key=True, on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.bio

    def get_absolute_url(self):
        user = User.objects.get(pk=self.id)
        return reverse("bio", args=[str(user)])


class Phone(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    user = models.OneToOneField(
        User, related_name="phone", primary_key=True, on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.phone


class GitHubAccount(models.Model):
    github = models.CharField(max_length=50)
    user = models.OneToOneField(
        User, related_name="github", primary_key=True, on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.github

    def save(self, *args, **kwargs):
        self.github = f"https://github.com/{self.github}"
        return super().save(*args, **kwargs)


class Skills(models.Model):
    skill = models.CharField(max_length=150, unique=True)
    user = models.OneToOneField(
        User, related_name="skills", primary_key=True, on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.skill

    @property
    def get_skills(self):
        skills = self.skill.split(",")
        skills.pop(-1)
        return skills

    def save(self, *args, **kwargs):
        self.skill = self.skill.title()
        return super().save(*args, **kwargs)


class Address(models.Model):
    country = models.CharField(max_length=50, verbose_name="Country")
    city = models.CharField(max_length=50, verbose_name="City")
    user = models.OneToOneField(
        User,
        related_name="address",
        primary_key=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    def __str__(self):
        return self.country

    def save(self, *args, **kwargs):
        self.country = self.country.title()
        self.city = self.city.title()
        return super().save(*args, **kwargs)

    @property
    def get_full_address(self):
        return f"{self.city}, {self.country}"

    @property
    def get_country(self):
        return self.country

    @property
    def get_city(self):
        return self.city
