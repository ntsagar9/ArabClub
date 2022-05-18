from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from logging_manager import eventslog
from newsfeed.models import Post
from newsfeed.serializer import (
    PostListSerializer,
    PostSerializer,
    PostUpdateSerializer,
)
from permissions.permissions import IsOwner

logger = eventslog.logger


class PostListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_queryset(count):
        return get_list_or_404(Post.objects.all()[:count])

    def get(self, request, count=20):
        obj = self.get_queryset(int(count))

        serializer = PostListSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data["user_id"] = request.user.pk
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailsView(APIView):
    permission_classes = [IsOwner]

    def get_object(self, request, pk):
        obj = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, slug, pk):
        obj = self.get_object(request, pk)
        serializer = PostSerializer(obj)
        return Response(serializer.data)

    def put(self, request, slug, pk):
        serializer = PostUpdateSerializer(data=request.data)
        obj = self.get_object(request, pk)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
            return Response(serializer.data)
        logger.error(f"{serializer.errors} - {request.user}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, pk):
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
