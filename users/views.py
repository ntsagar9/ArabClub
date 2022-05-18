# Url start is "account/"
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from logging_manager import eventslog
from permissions.permissions import IsAdminUser, IsOwner
from users.serializers import CreateUserSerializer, UserSerializer

user_model = get_user_model()
logger = eventslog.logger


class ListUserView(APIView):
    """
    Admin user only to access this is view
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        # me.create_user()    auto crate user for testing
        users = user_model.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info(f"{request} - {request.user}")
        return Response(serializer.data)


# View data specific user
class UserDetailsView(APIView):
    permission_classes = [IsOwner]

    def get_object(self, username):
        obj = get_object_or_404(user_model, username=username)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, username):
        obj = self.get_object(username)
        serializer = UserSerializer(obj, context={"request": request})
        return Response(serializer.data)

    def put(self, request, username):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object(username)
            serializer.update(user, serializer.validated_data)
            return Response(serializer.data, status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            logger.info(
                "{} - Just joined".format(
                    serializer.validated_data.get("username")
                )
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
