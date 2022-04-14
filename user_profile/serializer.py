import re

from rest_framework import serializers

from user_profile.models import (
    Name,
    Bio,
    Phone,
    Skills,
    GitHubAccount,
    Address,
)


# User First name and last name serializers with custom update data method
class NameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = Name
        fields = ["first_name", "last_name"]

    def update(self, instance, validated_data):
        try:
            instance = Name.objects.get(user_id=instance.pk)
        except Name.DoesNotExist:
            return Name.objects.create(**validated_data, user_id=instance.pk)

        instance.first_name = validated_data.get("first_name",
                                                 instance.first_name)
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
            return Bio.objects.create(**validated_data, user_id=instance.pk)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


# User skills serializers
class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ["skill"]

    @staticmethod
    def validate_skill(skill):
        pattern = re.compile(r'^([a-zA-Z]+,)+|(,)$')
        if re.fullmatch(pattern, skill):
            return skill
        raise serializers.ValidationError("Enter Valid Skill ex. python,js,")

    def update(self, instance, validated_data):
        try:
            instance = Skills.objects.get(user_id=instance.pk)
        except Skills.DoesNotExist:
            return Skills.objects.create(**validated_data, user_id=instance.pk)

        instance.skill = validated_data.get("skill",
                                            instance.skill)
        instance.save()
        return instance


# User address serializers with custom update data method
class AddressSerializer(serializers.ModelSerializer):
    # country = serializers.CharField(max_length=50)
    # city = serializers.CharField(max_length=50)

    class Meta:
        model = Address
        fields = ["country", "city"]

    def update(self, instance, validated_data):
        try:
            instance = Address.objects.get(user_id=instance.pk)
        except Address.DoesNotExist:
            return Address.objects.create(**validated_data, user_id=instance.pk)

        instance.country = validated_data.get("country", instance.country)
        instance.city = validated_data.get("city", instance.city)

        instance.save()
        return instance


# User GitHub Account serializers
class GitHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubAccount
        fields = ["github"]

    def update(self, instance, validated_data):
        try:
            instance = GitHubAccount.objects.get(user_id=instance.pk)
        except GitHubAccount.DoesNotExist:
            return GitHubAccount.objects.create(**validated_data,
                                                user_id=instance.pk)
        instance.github = validated_data.get("github", instance.github)
        instance.save()
        return instance


# User phone number serializers
class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["phone"]

    def validate_phone(self, phone):
        pattern = re.compile(r"[0-9]{11,15}")
        if re.fullmatch(pattern, phone):
            return phone
        raise serializers.ValidationError(
            "Please enter your phone number " "correctly."
        )

    def update(self, instance, validated_data):
        try:
            instance = Phone.objects.get(user_id=instance.pk)
        except Phone.DoesNotExist:
            return Phone.objects.create(**validated_data, user_id=instance.pk)

        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance
