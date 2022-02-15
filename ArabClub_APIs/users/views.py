# Url start is "account/"
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import (
    FirstNameAndLastName,
    Bio,
    Skills,
    Address,
    GitHubAccount,
    Phone
)
from users.serializers import (
    CustomSerializerUser,
    UpdateUserSerializer,
    UpdateNamesSerializer,
    BioSerializer,
    SkillsSerializer,
    AddressSerializer,
    GitHubSerializer,
    PhoneSerializer
)

# from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


# TODO
"""
Create Login, Register API
update profile API
"""


class ListUserView(APIView):

    def get(self, request):
        users = get_user_model()
        users = users.objects.all()
        serializer = CustomSerializerUser(users)
        return Response(serializer.data)


class UserDetailsView(APIView):

    @staticmethod
    def get_object(username):
        user = get_user_model()
        try:
            user = user.objects.get(username=username)
        except user.DoesNotExist:
            return ValueError(user.DoesNotExist)
        return user

    @staticmethod
    def get_user_object(request):
        obj = get_user_model()
        obj = obj.objects.get(pk=request.user.pk)
        return obj

    def get(self, request, username):
        user = self.get_object(username)
        serializer = CustomSerializerUser(user)
        if serializer.err:
            return Response(serializer.err)
        return Response(serializer.data)

    def put(self, request, username):
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = self.get_user_object(request)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data)


class PersonInfoView(APIView):
    def get_object(self):
        try:
            obj = FirstNameAndLastName.objects.get(user_id=self.request.user.id)
            return obj
        except FirstNameAndLastName.DoesNotExist:
            pass

    def get(self, request, username):
        obj = self.get_object()
        serializer = UpdateNamesSerializer(obj)
        return Response(serializer.data)

    def put(self, request, username):
        self.request.data['user_id'] = request.user.id
        serializer = UpdateNamesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        model = FirstNameAndLastName(user_id=request.user.pk)
        serializer.update(model, serializer.validated_data)
        return Response(serializer.data)


class BioView(APIView):
    def get_object(self):
        try:
            bio = Bio.objects.get(user_id=self.request.user.id)
            return bio
        except Bio.DoesNotExist:
            pass

    def get(self, request, username):
        bio = self.get_object()
        serializer = BioSerializer(bio)
        return Response(serializer.data)

    def put(self, request, username):
        self.request.data['user_id'] = request.user.id
        serializer = BioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Bio.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)


class SkillsView(APIView):

    def get_object(self):
        try:
            obj = Skills.objects.all().filter(user_id=self.request.user.id)
            return obj
        except Skills.DoesNotExist:
            pass

    def get(self, request, username):
        obj = self.get_object()
        serializer = SkillsSerializer(obj, many=True)
        return Response(serializer.data)

    def put(self, request, username):
        for skill in request.data:
            serializer = SkillsSerializer(data=skill)
            if not serializer.is_valid():
                return Response(serializer.errors)

            try:
                obj = Skills.objects.get(id=skill['id'])
            except KeyError:
                Skills.objects.create(**skill)
                continue

            if obj.skill_name == skill['skill_name']:
                continue
            serializer.update(obj, serializer.validated_data)
        serializer = SkillsSerializer(self.get_object(), many=True)
        return Response(serializer.data)


class AddressView(APIView):

    def get(self, request, username):
        obj = Address.objects.get(user_id=request.user.id)
        serializer = AddressSerializer(obj)
        return Response(serializer.data)

    def put(self, request, username):
        request.data['user_id'] = request.user.id
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Address.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)


class GitHubView(APIView):
    def get(self, request, username):
        obj = GitHubAccount.objects.get(user_id=request.user.id)
        serializer = GitHubSerializer(obj)
        return Response(serializer.data)

    def put(self, request, username):
        request.data['user_id'] = request.user.id
        serializer = GitHubSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = GitHubAccount.objects.get(user_id=request.user.id)
        serializer.update(obj, request.data)
        return Response(serializer.data)


class PhoneView(APIView):
    def get(self, request, username):
        obj = Phone.objects.get(user_id=request.user.id)
        serializer = PhoneSerializer(obj)
        return Response(serializer.data)

    def put(self, request, username):
        request.data['user_id'] = request.user.id
        serializer = PhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Phone.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)
