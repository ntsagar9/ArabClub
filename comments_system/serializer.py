from django.utils import timezone
from rest_framework import serializers

from comments_system.models import (Comment, Reply)
from users.serializers import UserShortSerializer


class ReplySerializer(serializers.ModelSerializer):
    """
    Reply serializer with relation data from post and user
    """

    class Meta:
        model = Reply
        fields = ["pk", "reply", "comment", "user"]

    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        return reply


class CommentSerializer(serializers.ModelSerializer):
    """comment serializer with relation data from reply and user post"""

    replys_comment = ReplySerializer(many=True, required=False)
    user = UserShortSerializer(required=False)

    def __init__(self, request=None, **kwargs):
        super(CommentSerializer, self).__init__(**kwargs)
        self.request = request

    class Meta:
        model = Comment
        fields = [
            "pk",
            "comment",
            "create_at",
            "update_at",
            "post",
            "user",
            "replys_comment",
        ]

    def create(self, validated_data):
        obj = Comment.objects.create(**validated_data,
                                     user_id=self.request.user.pk)
        return obj


class CommentUpdateSerializer(serializers.ModelSerializer):
    """ Comment update with none post_id, user_id
    but auto add by server not client"""
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["comment", "post", "user"]
        extra_kwargs = {"post": {"required": False},
                        "user": {"required": False}}

    def update(self, instance, validated_data):
        instance.comment = validated_data.get("comment", instance.comment)
        instance.update_at = timezone.now()
        instance.save()
        return instance
