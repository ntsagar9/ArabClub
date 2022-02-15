from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import (
    FirstNameAndLastName, Phone, Bio, Address, GitHubAccount, Skills
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'date_of_birth']


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'date_of_birth']

    def update(self, instance, validate_date):
        instance.username = validate_date.get('username', instance.username)
        instance.email = validate_date.get('email', instance.email)
        instance.date_of_birth = validate_date.get('date_of_birth',
                                                   instance.date_of_birth)
        instance.save()
        return instance

    @classmethod
    def get_model(cls):
        return cls.Meta.model


class UpdateNamesSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = FirstNameAndLastName
        fields = ['first_name', 'last_name', 'user_id']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance

    @classmethod
    def get_model(cls, user_id):
        obj = cls.Meta.model.objects.get(user_id=user_id)
        return obj


class BioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bio
        fields = ['bio', 'user_id']

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class SkillsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Skills
        fields = ['id', 'skill_name', 'user_id']


class AddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False)
    street_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Address
        fields = ['country', 'city', 'street_name', 'user_id']

    def update(self, instance, validated_data):
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.street_name = validated_data.get('street_name',
                                                  instance.street_name)
        instance.save()
        return instance


class GitHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubAccount
        fields = ['url', 'user_id']

    serializer_url_field = 'url'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['phone', 'user_id']


class CustomSerializerUser:
    """
    Get all data for users and set values to list
    """

    def __init__(self, obj):
        self.obj = obj
        self.data = []
        self.index = -1
        self.id = 0
        self.err = False
        try:
            self.get_basic_data_for_many()
        except Exception as e:
            self.get_basic_data_for_single()

    def get_basic_data_for_single(self) -> list:
        try:
            self.id = self.obj.id
        except AttributeError:
            self.err = '[Errors 01] 404 user not found'
            return self.err

        self.index += 1
        self.data.append({'id': self.id, 'username': self.obj.username})
        bio = self.bio
        self.data[self.index]['birthdate'] = self.obj.date_of_birth
        self.get_person_info()
        self.get_address()
        self.get_skills()
        self.get_phone()
        self.get_github()

        return self.data

    def get_basic_data_for_many(self):
        for user in self.obj:
            self.id = user.id
            self.index += 1
            self.data.append({'id': self.id, 'username': user.username})
            bio = self.bio
            self.data[self.index]['birthdate'] = user.date_of_birth
            self.get_person_info()
            self.get_address()
            self.get_skills()
            self.get_phone()
            self.data[self.index]['person_info']['connect']['email'] = \
                user.email

            self.get_github()

        return self.data

    @property
    def bio(self):
        try:
            bio = Bio.objects.get(user_id=self.id)
            self.data[self.index]['bio'] = bio.bio
        except Bio.DoesNotExist:
            pass

    def get_person_info(self):
        try:
            names = FirstNameAndLastName.objects.get(user_id=self.id)
            self.data[self.index]['person_info'] = {
                'first_name': names.first_name,
                'last_name': names.last_name,
            }
        except FirstNameAndLastName.DoesNotExist:
            pass

    def get_github(self):
        try:
            github = GitHubAccount.objects.get(user_id=self.id)
            self.data[self.index]['github'] = github.url
        except GitHubAccount.DoesNotExist:
            pass

    def get_phone(self):
        try:
            phone = Phone.objects.get(user_id=self.id)
            self.data[self.index]['person_info']['connect'] = {
                'phone': phone.phone}
        except Phone.DoesNotExist:
            pass

    def get_skills(self):
        try:
            skills = Skills.objects.all().filter(user_id=self.id)
            if skills.__len__() > 0:
                self.data[self.index]['skills'] = [
                    skill.skill_name for skill in skills
                ]
        except Skills.DoesNotExist:
            pass

    def get_address(self):
        try:
            address = Address.objects.get(user_id=self.id)
            self.data[self.index]['person_info'][
                'address'] = address.get_full_address
        except Address.DoesNotExist:
            pass
