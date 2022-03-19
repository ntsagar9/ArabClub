from rest_framework import serializers

from comments_system.models import (Comment, Reply)
from users.serializers import UserShortSerializer


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
                    **validated_data, user_id=self.request.user.pk,
                    comment_id=path[-1]
                )
                return obj
            except django.db.utils.IntegrityError:
                raise serializers.ValidationError("Comment Not Found 404.")
        raise serializers.ValidationError("Please give me request.!")


class CommentSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        instance.post_comment_fk = validated_data.get(instance.post_id)
        instance.user_comment_fk = validated_data.get(instance.user_id)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.update_at = timezone.now()
        instance.save()
        return instance

    def create(self, validated_data):
        obj = Comment.objects.create(**validated_data,
                                     user_id=self.request.user.pk)
        return obj


class CommentUpdateSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["comment", "post", "user"]
        extra_kwargs = {"post": {"required": False},
                        "user": {"required": False}}

    def update(self, instance, validated_data):
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance
