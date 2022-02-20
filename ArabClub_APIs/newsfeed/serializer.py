from rest_framework import serializers

from newsfeed.models import Post, Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name', 'post_id']


class PostSerializer(serializers.ModelSerializer):
    # post_tags = TagsSerializer(required=False, many=True)
    post_tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_tags', 'create_data', 'update',
                  'user_id']
