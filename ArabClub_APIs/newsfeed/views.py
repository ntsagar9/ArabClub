from django.shortcuts import render
from rest_framework.views import  APIView
from newsfeed.serializer import PostSerializer
from django.shortcuts import get_list_or_404
from newsfeed.models import Post
from rest_framework.response import Response


class PostListView(APIView):

    def get_objects(self):
        obj = get_list_or_404(Post)
        return obj

    def get(self, request):
        data = self.get_objects()
        serializer = PostSerializer(data, many=True)
        return Response(serializer.data)