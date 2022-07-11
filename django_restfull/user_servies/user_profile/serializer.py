"""
this serializers for update or create if info not exist
for specify user
"""
import re

from rest_framework import serializers

from user_profile.models import (
    Address,
    Bio,
    GitHubAccount,
    Name,
    Phone,
    Skills,
)


class NameSerializer(serializers.ModelSerializer):
    """user information serializers for only names"""

    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = Name
        fields = ["first_name", "last_name"]

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = Name.objects.get(user_id=instance.pk)
        except Name.DoesNotExist:
            # Create new info
            return Name.objects.create(**validated_data, user_id=instance.pk)

        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.save()
        return instance


# User Bio serializers with custom update data method
class BioSerializer(serializers.ModelSerializer):
    """
    user information serializers for only bio
    """

    class Meta:
        model = Bio
        fields = ["bio"]

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = Bio.objects.get(user_id=instance.pk)
        except Bio.DoesNotExist:
            # Crate new info
            return Bio.objects.create(**validated_data, user_id=instance.pk)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


# User skills serializers
class SkillsSerializer(serializers.ModelSerializer):
    """
    user information serializers for only skills
    """

    class Meta:
        model = Skills
        fields = ["skill"]

    @staticmethod
    def validate_skill(skill):
        """Validate skill pattern"""
        pattern = re.compile(r"^([a-zA-Z]+,)+|(,)$")
        if re.fullmatch(pattern, skill):
            return skill
        raise serializers.ValidationError("Enter Valid Skill ex. python,js,")

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = Skills.objects.get(user_id=instance.pk)
        except Skills.DoesNotExist:
            # Create new info
            return Skills.objects.create(**validated_data, user_id=instance.pk)

        instance.skill = validated_data.get("skill", instance.skill)
        instance.save()
        return instance


# User address serializers with custom update data method
class AddressSerializer(serializers.ModelSerializer):
    """
    user information serializers for only Address
    """

    class Meta:
        model = Address
        fields = ["country", "city"]

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = Address.objects.get(user_id=instance.pk)
        except Address.DoesNotExist:
            # Create new info
            return Address.objects.create(
                **validated_data, user_id=instance.pk
            )

        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)

        instance.save()
        return instance


# User GitHub Account serializers
class GitHubSerializer(serializers.ModelSerializer):
    """
    user information serializer for only GitHub
    """

    class Meta:
        model = GitHubAccount
        fields = ["github"]

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = GitHubAccount.objects.get(user_id=instance.pk)
        except GitHubAccount.DoesNotExist:
            # Crate new info
            return GitHubAccount.objects.create(
                **validated_data, user_id=instance.pk
            )
        instance.github = validated_data.get("github", instance.github)
        instance.save()
        return instance


# User phone number serializers
class PhoneSerializer(serializers.ModelSerializer):
    """
    user information serializer for only phone number
    """

    class Meta:
        model = Phone
        fields = ["phone"]

    def validate_phone(self, phone):
        """Check phone is validate with patterns"""
        pattern = re.compile(r"[0-9]{11,15}")
        if re.fullmatch(pattern, phone):
            return phone
        raise serializers.ValidationError(
            "Please enter your phone number " "correctly."
        )

    def update(self, instance, validated_data):
        """
        update current user information if exist
        or create new data for current user
        """
        try:
            # Update info
            instance = Phone.objects.get(user_id=instance.pk)
        except Phone.DoesNotExist:
            # Create new info
            return Phone.objects.create(**validated_data, user_id=instance.pk)

        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance
