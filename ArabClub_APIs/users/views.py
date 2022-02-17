# Url start is "account/"
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import (
    FirstNameAndLastName,
    Bio,
    Skills,
    Address,
    GitHubAccount,
    Phone,
)
from users.serializers import (
    BioSerializer,
    SkillsSerializer,
    AddressSerializer,
    GitHubSerializer,
    PhoneSerializer,
    # New
    UserSerializer,
)


# List All User endpoint with custom format
# Done
class ListUserView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = get_user_model()
        users = users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# View data specific user
class UserDetailsView(APIView):
    # permission_classes = [IsOwner]

    # Start Old Code
    # def get_object(self, username):
    #     user = get_user_model()
    #     obj = get_object_or_404(user, username=username)
    #     self.check_object_permissions(self.request, obj)
    #     return obj
    #
    # def get(self, request, username):
    #     user = self.get_object(username)
    #     serializer = CustomSerializerUser(user)
    #     if serializer.err:
    #         return Response(serializer.err)
    #     return Response(serializer.data)
    #
    # def put(self, request, username):
    #     serializer = UpdateUserSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors)
    #     user = self.get_object(username)
    #     serializer.update(user, serializer.validated_data)
    #     return Response(serializer.data)
    # End Old Code

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None

    def get_object(self):
        model = get_user_model()
        obj = get_object_or_404(model, username=self.username)
        return obj

    def get(self, request, username):
        self.username = username
        obj = self.get_object()
        serializer = UserSerializer(obj, context={"request": request})
        return Response(serializer.data)

    def put(self, request, username):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model()
            user = user.objects.get(pk=request.user.id)
            serializer.update(user, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view person info for specific user
class PersonInfoView(APIView):
    def get_object(self):
        try:
            obj = FirstNameAndLastName.objects.get(user_id=self.request.user.id)
            return obj
        except FirstNameAndLastName.DoesNotExist:
            pass

    def get(self, request, **kwargs):
        obj = self.get_object()
        serializer = UpdateNamesSerializer(obj)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        self.request.data["user_id"] = request.user.id
        serializer = UpdateNamesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        model = FirstNameAndLastName(user_id=request.user.pk)
        serializer.update(model, serializer.validated_data)
        return Response(serializer.data)


# view bio for specific user
class BioView(APIView):
    def get_object(self):
        try:
            bio = Bio.objects.get(user_id=self.request.user.id)
            return bio
        except Bio.DoesNotExist:
            pass

    def get(self, request, **kwargs):
        bio = self.get_object()
        serializer = BioSerializer(bio)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        self.request.data["user_id"] = request.user.id
        serializer = BioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Bio.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)


# view skills for specific user
class SkillsView(APIView):
    def get_object(self):
        try:
            obj = Skills.objects.all().filter(user_id=self.request.user.id)
            return obj
        except Skills.DoesNotExist:
            pass

    def get(self, request, **kwargs):
        obj = self.get_object()
        serializer = SkillsSerializer(obj, many=True)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        for skill in request.data:
            serializer = SkillsSerializer(data=skill)
            if not serializer.is_valid():
                return Response(serializer.errors)

            try:
                obj = Skills.objects.get(id=skill["id"])
            except KeyError:
                Skills.objects.create(**skill)
                continue

            if obj.skill_name == skill["skill_name"]:
                continue
            serializer.update(obj, serializer.validated_data)
        serializer = SkillsSerializer(self.get_object(), many=True)
        return Response(serializer.data)


# view address for specific user
class AddressView(APIView):
    def get(self, request, **kwargs):
        obj = Address.objects.get(user_id=request.user.id)
        serializer = AddressSerializer(obj)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        request.data["user_id"] = request.user.id
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Address.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)


# view github account for specific user
class GitHubView(APIView):
    def get(self, request, **kwargs):
        obj = GitHubAccount.objects.get(user_id=request.user.id)
        serializer = GitHubSerializer(obj)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        request.data["user_id"] = request.user.id
        serializer = GitHubSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = GitHubAccount.objects.get(user_id=request.user.id)
        serializer.update(obj, request.data)
        return Response(serializer.data)


# view phone number for specific user
class PhoneView(APIView):
    def get(self, request, **kwargs):
        obj = Phone.objects.get(user_id=request.user.id)
        serializer = PhoneSerializer(obj)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        request.data["user_id"] = request.user.id
        serializer = PhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        obj = Phone.objects.get(user_id=request.user.id)
        serializer.update(obj, serializer.validated_data)
        return Response(serializer.data)
