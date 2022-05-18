import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from logging_manager import eventslog
from tag_system.serializer import FollowTagsSerializers
from user_profile.serializer import (
    AddressSerializer,
    BioSerializer,
    GitHubSerializer,
    NameSerializer,
    PhoneSerializer,
    SkillsSerializer,
)

logger = eventslog.logger


def auto_try(func):
    """
    Exception any errors
    """

    def run(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return e

    return run


class UserSerializer(serializers.ModelSerializer):
    """
    Update all information for users from one end point
    this class can call all related others classes with 'other func'
    each class is responsible for updating the information about
    """

    bio = BioSerializer(required=False)
    phone = PhoneSerializer(required=False)
    skills = SkillsSerializer(required=False)
    name = NameSerializer(required=False)
    address = AddressSerializer(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    date_of_birth = serializers.DateField(required=False)
    github = GitHubSerializer(required=False)
    follow_tag = FollowTagsSerializers(required=False, many=True)

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
            "github",
            "phone",
            "address",
            "follow_tag",
        ]

    @staticmethod
    def validate_username(username):
        pattern = re.compile(
            r"^[a-zA](?=[a-zA-Z\d._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        )

        if re.fullmatch(pattern, username):
            return username
        raise serializers.ValidationError("Enter valid username ex. xxxx.xxxx")

    def update(self, instance, validated_data):
        """
        Update main information for each user
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        # updating other information
        self.other(instance, validated_data)
        instance.save()
        return instance

    def other(self, instance, validated_data):
        """
        Can update other information if request include other information
        """
        for k in [*validated_data]:
            match k:
                case "follow_tag":
                    self.update_follow_tag(instance, validated_data[k])
                case "name":
                    self.update_name(instance, validated_data[k])
                case "bio":
                    self.update_bio(instance, validated_data[k])
                case "phone":
                    self.update_phone(instance, validated_data[k])
                case "github":
                    self.update_github_url(instance, validated_data[k])
                case "address":
                    self.update_address(instance, validated_data[k])
                case "skills":
                    self.update_skills(instance, validated_data[k])

    # Every function responsible is update its part from information
    @auto_try
    def update_github_url(self, instance, validated_data):
        serializer = GitHubSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        return serializer.errors

    @auto_try
    def update_phone(self, instance, validated_data):
        serializer = PhoneSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        return serializer.errors

    @auto_try
    def update_address(self, instance, validated_data):
        serializer = AddressSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        return serializer.errors

    @auto_try
    def update_skills(self, instance, validated_data):
        serializer = SkillsSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        return serializer.errors

    @auto_try
    def update_bio(self, instance, validated_data):
        serializer = BioSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        return serializer.errors

    @auto_try
    def update_name(self, instance, validated_data):
        serializer = NameSerializer(data=validated_data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
        else:
            raise serializer.errors

    @auto_try
    def update_follow_tag(self, instance, validated_data):
        data = [{key: tag[key].pk} for tag in validated_data for key in tag]
        serializer = FollowTagsSerializers(data=data, many=True)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return serializer.data
        return serializer.errors


class UserShortSerializer(serializers.ModelSerializer):
    name = NameSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ["pk", "name"]


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
            r"^[a-zA](?=[a-zA-Z\d._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
        )

        if re.fullmatch(pattern, username):
            return username

        raise serializers.ValidationError("Enter valid username ex. xxxx.xxxx")

    def create(self, validated_data):
        user = get_user_model()
        user.objects.create_user(**validated_data)
        return user
