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


# User First name and last name serializers with custom update data method
class NameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = FirstNameAndLastName
        fields = ["first_name", "last_name"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.save()
        return instance

    @classmethod
    def get_model(cls, user_id):
        obj = cls.Meta.model.objects.get(user_id=user_id)
        return obj


# User Bio serializers with custom update data method
class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ["bio"]

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


# User skills serializers
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ["skill_name"]


# User address serializers with custom update data method
class AddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False)
    street_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Address
        fields = ["country", "city", "street_name"]

    def update(self, instance, validated_data):
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
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
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
        self.update_name(instance, validated_data)
        self.update_bio(instance, validated_data)
        self.update_skills(instance, validated_data)
        self.update_address(instance, validated_data)
        self.update_phone(instance, validated_data)
        self.update_github_url(instance, validated_data)
        instance.save()
        return instance

    def update_github_url(self, instance, validated_data):
        try:
            github_data = validated_data.pop("github_url")
            if not GitHubAccount.objects.update(user_id=instance.id, **github_data):
                GitHubAccount.objects.create(user_id=instance.id)
        except KeyError:
            pass

    def update_phone(self, instance, validated_data):
        try:
            phone_data = validated_data.pop("phone")
            if not Phone.objects.update(user_id=instance.id, **phone_data):
                Phone.objects.create(user_id=instance.id, **phone_data)
        except KeyError:
            pass

    def update_address(self, instance, validated_data):
        try:
            address_data = validated_data.pop("address")
            if not Address.objects.update(user_id=instance.id, **address_data):
                Address.objects.create(user_id=instance.id, **address_data)
        except KeyError:
            pass

    def update_skills(self, instance, validated_data):
        try:
            skill_data = validated_data.pop("skills")
            if not Skills.objects.update(user_id=instance.id, **skill_data):
                Skills.objects.create(user_id=instance.id, **skill_data)
        except KeyError:
            pass

    def update_bio(self, instance, validated_data):
        try:
            bio_data = validated_data.pop("bio")
            if not Bio.objects.update(user_id=instance.id, **bio_data):
                Bio.objects.create(user_id=instance.id, **bio_data)
        except KeyError:
            pass

    def update_name(self, instance, validated_data):
        try:
            name_data = validated_data.pop("name")

            if not FirstNameAndLastName.objects.update(
                user_id=instance.id, **name_data
            ):
                FirstNameAndLastName.objects.create(user_id=instance.id, **name_data)
        except KeyError:
            pass
