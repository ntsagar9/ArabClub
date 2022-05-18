from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from comments_system.models import Comment, Reply
from comments_system.serializer import (
    CommentSerializer,
    CommentUpdateSerializer,
    ReplySerializer,
)
from logging_manager import eventslog
from permissions.permissions import IsOwner

logger = eventslog.logger


class CommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_object(pk):
        obj = get_list_or_404(Comment, pk=pk)
        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = CommentSerializer(obj, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data, request=request)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDetailView(APIView):
    permission_classes = [IsOwner]

    @staticmethod
    def get_object(pk):
        obj = get_object_or_404(Comment, pk=pk)
        return obj

    def put(self, request, pk):
        serializer = CommentUpdateSerializer(data=request.data)
        obj = self.get_object(pk)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelpyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly and IsOwner]

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = ReplySerializer(obj)
        return Response(serializer.data)

    def post(self, request, pk):
        self.add_required_fields(pk, request)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = self.get_object(pk)
        self.add_required_fields(pk, request)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def add_required_fields(pk, request):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            comment = Comment.objects.get(replys_comment=pk)
        request.data["user"] = request.user.pk
        request.data["comment"] = comment.id

    @staticmethod
    def get_object(pk):
        obj = get_object_or_404(Reply, id=pk)
        return obj
