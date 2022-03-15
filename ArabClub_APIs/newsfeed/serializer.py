import django.db.utils
from django.utils import timezone
from rest_framework import serializers

from newsfeed.models import Post, Tag, Comments, Reply
from users.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_name", "post_id"]


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(read_only=True)

    def __init__(self, instance=None, request=None, **kwargs):
        self.request = request
        if not len(kwargs):
            super(ReplySerializer, self).__init__(instance)
        else:
            super(ReplySerializer, self).__init__(**kwargs)

    class Meta:
        model = Reply
        fields = ["pk", "reply", "comment", "user_id"]

    def create(self, validated_data):
        path = self.request.path.split("/")
        if self.request is not None:
            try:
                obj = Reply.objects.create(
                    **validated_data, user_id=self.request.user.pk, comment_id=path[-1]
                )
                return obj
            except django.db.utils.IntegrityError:
                raise serializers.ValidationError("Comment Not Found 404.")
        raise serializers.ValidationError("Please give me request.!")


class CommentSerializer(serializers.ModelSerializer):
    reply_comment_fk = ReplySerializer(many=True, required=False)
    user = UserSerializer(required=False)

    def __init__(self, request=None, **kwargs):
        super(CommentSerializer, self).__init__(**kwargs)
        self.request = request

    class Meta:
        model = Comments
        fields = [
            "pk",
            "comment",
            "create_at",
            "update_at",
            "post",
            "user",
            "reply_comment_fk",
        ]

    def update(self, instance, validated_data):
        instance.post_comment_fk = validated_data.get(instance.post_id)
        instance.user_comment_fk = validated_data.get(instance.user_id)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.update_at = timezone.now()
        instance.save()
        return instance

    def create(self, validated_data):
        obj = Comments.objects.create(**validated_data, user_id=self.request.user.pk)
        return obj


class CommentUpdateSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ["comment", "post", "user"]
        extra_kwargs = {"post": {"required": False}, "user": {"required": False}}

    def update(self, instance, validated_data):
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    post_tags = TagsSerializer(many=True, read_only=True)
    post_comment_fk = CommentSerializer(many=True, read_only=True)
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
            "post_comment_fk",
        ]

    def create(self, validated_data):
        title = validated_data.get("title")
        post = Post.objects.create(**validated_data, slug=title.replace(" ", "-"))
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)


class PostUpdateSerializer(serializers.ModelSerializer):
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
