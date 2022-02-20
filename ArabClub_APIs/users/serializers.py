import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import (
    FirstNameAndLastName,
    Phone,
    Bio,
    Address,
    GitHubAccount,
    Skills,
)


def try_auto(func):
    def run(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            return e

    return run


# User First name and last name serializers with custom update data method
class NameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = FirstNameAndLastName
        fields = ["first_name", "last_name"]

    def update(self, instance, validated_data):
        try:
            instance = FirstNameAndLastName.objects.get(user_id=instance.pk)
        except FirstNameAndLastName.DoesNotExist:
            return FirstNameAndLastName.objects.create(**validated_data)

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


# User Bio serializers with custom update data method
class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ["bio"]

    def update(self, instance, validated_data):
        try:
            instance = Bio.objects.get(user_id=instance.pk)
        except Bio.DoesNotExist:
            return Bio.objects.create(**validated_data)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


# User skills serializers
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ["skill_name"]

    def update(self, instance, validated_data):
        try:
            instance = Skills.objects.get(user_id=instance.pk)
        except Skills.DoesNotExist:
            return Skills.objects.create(**validated_data)

        instance.skill_name = validated_data.get("skill_name", instance.skill_name)
        instance.save()
        return instance


# User address serializers with custom update data method
class AddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False)
    street_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Address
        fields = ["country", "city", "street_name"]

    def update(self, instance, validated_data):
        try:
            instance = Address.objects.get(user_id=instance.pk)
        except Address.DoesNotExist:
            instance = Address.objects.create(**validated_data)
            return instance
        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)
        instance.street_name = validated_data.get("street_name", instance.street_name)
        instance.save()
        return instance


# User GitHub Account serializers
class GitHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubAccount
        fields = ["url"]

    def update(self, instance, validated_data):
        try:
            instance = GitHubAccount.objects.get(user_id=instance.pk)
        except GitHubAccount.DoesNotExist:
            return GitHubAccount.objects.create(**validated_data)

        instance.url = validated_data.get("url", instance.url)
        instance.save()
        return instance


# User phone number serializers
class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["phone"]

    def validate_phone(self, phone):
        pattern = r"[0-9]{11,15}"
        re.compile(pattern)
        if re.fullmatch(pattern, phone):
            return phone
        raise serializers.ValidationError(
            "Please enter your phone number " "correctly."
        )

    def update(self, instance, validated_data):
        try:
            instance = Phone.objects.get(user_id=instance.pk)
        except Phone.DoesNotExist:
            return Phone.objects.create(**validated_data)

        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    This is main serializer
    return:
    user info
    bio
    phone
    skills
    GitHub
    """

    bio = BioSerializer(required=False)
    phone = PhoneSerializer(required=False)
    skills = SkillsSerializer(required=False)
    name = NameSerializer(required=False)
    address = AddressSerializer(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    date_of_birth = serializers.DateField(required=False)
    github_url = GitHubSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "name",
            "username",
            "email",
            "date_of_birth",
            "bio",
            "skills",
            "github_url",
            "phone",
            "address",
        ]

    def validate_username(self, username):
        pattern = re.compile(
            r"^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        )

        if re.fullmatch(pattern, username):
            return username

        raise serializers.ValidationError("Enter valid username ex. xxxx.xxxx")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        self.other(instance, validated_data)
        instance.save()
        return instance

    def other(self, instance, validated_data):
        self.update_name(instance, validated_data)
        self.update_bio(instance, validated_data)
        self.update_skills(instance, validated_data)
        self.update_address(instance, validated_data)
        self.update_phone(instance, validated_data)
        self.update_github_url(instance, validated_data)

    @try_auto
    def update_github_url(self, instance, validated_data):
        validated_data = {
            "url": validated_data["github_url"]["url"],
            "user_id": instance.id,
        }
        GitHubSerializer.update(self, instance, validated_data)

    @try_auto
    def update_phone(self, instance, validated_data):
        validated_data = {
            "phone": validated_data["phone"]["phone"],
            "user_id": instance.id,
        }
        PhoneSerializer.update(self, instance, validated_data)

    @try_auto
    def update_address(self, instance, validated_data):
        validated_data = {
            "country": validated_data["address"]["country"],
            "city": validated_data["address"]["city"],
            "street_name": validated_data["address"]["street_name"],
            "user_id": instance.id,
        }
        AddressSerializer.update(self, instance, validated_data)

    @try_auto
    def update_skills(self, instance, validated_data):
        validated_data = {
            "skill_name": validated_data["skills"]["skill_name"],
            "user_id": instance.id,
        }
        SkillsSerializer.update(self, instance, validated_data)

    @try_auto
    def update_bio(self, instance, validated_data):
        validated_data = {"bio": validated_data["bio"]["bio"], "user_id": instance.id}
        BioSerializer.update(self, instance, validated_data)

    @try_auto
    def update_name(self, instance, validated_data):
        validated_data = {
            "first_name": validated_data["name"]["first_name"],
            "last_name": validated_data["name"]["last_name"],
            "user_id": instance.id,
        }
        NameSerializer.update(self, instance, validated_data)


class CreateUserSerializer(serializers.ModelSerializer):
    """
    This main serializer for create new user only
    """

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "date_of_birth", "password"]
        # make password field to write only,  required and not return
        # password in response
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def validate_username(self, username):
        pattern = re.compile(
            r"^[a-zA](?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        )

        if re.fullmatch(pattern, username):
            return username

        raise serializers.ValidationError("Enter valid username ex. xxxx.xxxx")

    def create(self, validated_data):
        user = get_user_model()
        user.objects.create_user(**validated_data)
        return user
