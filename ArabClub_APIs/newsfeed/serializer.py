from django.utils import timezone
from rest_framework import serializers

from newsfeed.models import Post, Tag, Comments, Reply


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name', 'post_id']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    reply_comment_fk = ReplySerializer(many=True, required=False)
    post_comment_fk = serializers.RelatedField(read_only=True)
    user_comment_fk = serializers.RelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ['pk', 'comment', 'create_at', 'update_at', 'post_comment_fk',
                  'user_comment_fk', 'reply_comment_fk']

    def update(self, instance, validated_data):
        instance.post_comment_fk = validated_data.get(instance.post_id)
        instance.user_comment_fk = validated_data.get(instance.user_id)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.update_at = timezone.now()
        instance.save()
        return instance


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_tags = TagsSerializer(many=True, read_only=True)
    post_comment_fk = CommentsSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_tags', 'published_at', 'update_at',
                  'status', 'user_id', 'post_comment_fk']

    def create(self, validated_data):
        title = validated_data.get('title')
        post = Post.objects.create(**validated_data,
                                   slug=title.replace(' ', '-'))
        return post
