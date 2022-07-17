from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from logging_manager import eventslog
from permissions.permissions import IsAdminUser, IsOwner
from user.serializers import UserSerializer

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
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response(serializer.data, status=status.HTTP_200_OK)
