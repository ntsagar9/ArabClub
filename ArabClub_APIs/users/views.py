# Url start is "account/"
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.models import FirstNameAndLastName


# TODO
"""
Create Login, Register API
update profile API
"""


class ListUserView(APIView):

    def get(self, request):
        users = get_user_model()
        users = users.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)