from rest_framework import serializers

from comments_system.serializer import CommentSerializer
from newsfeed.models import Post
from tag_system.serializer import TagsSerializer
from users.serializers import UserShortSerializer


class PostSerializer(serializers.ModelSerializer):
    """posts custom serializer with include tags and some user information"""

    post_tags = TagsSerializer(many=True, read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(required=True)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Post
        fields = [
            "pk",
            "title",
            "content",
            "slug",
            "post_tags",
            "published_at",
            "update_at",
            "status",
            "user_id",
            "post_comments",
        ]

    def create(self, validated_data):
        title = validated_data.get("title")
        post = Post.objects.create(
            **validated_data, slug=title.replace(" ", "-")
        )
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    """Post serializer for only update post date"""

    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


class PostListSerializer(serializers.ModelSerializer):
    """Post list serializer with limit data to optimize response"""

    user = UserShortSerializer(read_only=True)
    post_comments = Post.get_total_comments

    class Meta:
        model = Post
        fields = [
            "pk",
            "title",
            "published_at",
            "slug",
            "user",
            "post_comments",
        ]
