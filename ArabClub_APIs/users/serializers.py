from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import FirstNameAndLastName


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']
