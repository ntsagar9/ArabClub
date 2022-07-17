import re

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from tag_system.models import FollowTag
from user_profile.models import (
    Address,
    Bio,
    GitHubAccount,
    Name,
    Phone,
    Skills,
)
from user.models import User


class UserCreationFrom(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username", "date_of_birth", "is_active")

    def clean_username(self):
        # Check that the username is valid
        username = self.cleaned_data.get("username")
        is_valid = re.search(
            r"^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$",
            username,
        )
        if not is_valid:
            raise ValidationError("Enter Valid Username")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "date_of_birth",
            "is_active",
            "is_admin",
        )

    def clean_username(self):
        # Check that the username is valid
        username = self.cleaned_data.get("username")
        is_valid = re.search(
            r"^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$",
            username,
        )
        if not is_valid:
            raise ValidationError("Enter Valid Username")
        return username


class UserAddNamesForm(admin.TabularInline):
    """
    Form for user add first name and last name
    """

    model = Name


class UserPhone(admin.TabularInline):
    """
    Add Phone Number for user
    """

    model = Phone


class UserBio(admin.TabularInline):
    """
    Add Bio for user
    """

    model = Bio


class UserSkills(admin.TabularInline):
    """
    Add skills for user
    """

    model = Skills


class UserAddress(admin.TabularInline):
    """
    Add address for user
    """

    model = Address


class UserGitHub(admin.TabularInline):
    """
    Add GitHub account for user
    """

    model = GitHubAccount


class UserFollowTags(admin.TabularInline):
    model = FollowTag


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationFrom
    inlines = [
        UserAddNamesForm,
        UserPhone,
        UserBio,
        UserAddress,
        UserSkills,
        UserGitHub,
        UserFollowTags,
    ]

    # The fields to be used in displaying the User serializer.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "username", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("date_of_birth",)}),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_admin"),
            },
        ),
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "date_of_birth",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group serializer from admin.
admin.site.unregister(Group)
