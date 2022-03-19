from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from comments_system.models import Comment, Reply
from comments_system.serializer import (
    CommentSerializer,
    CommentUpdateSerializer,
    ReplySerializer
)
from users.permissions import IsOwner


class CommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, slug, pk):
        serializer = CommentSerializer(data=request.data, request=request)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
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
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RelpyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly and IsOwner]

    @staticmethod
    def get_object(pk):
        obj = get_object_or_404(Reply, id=pk)
        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = ReplySerializer(obj)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReplySerializer(request=request, data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_201_CREATED)
