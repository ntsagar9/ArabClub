from rest_framework import serializers

from tag_system.models import FollowTag, Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {"post": {"write_only": True, "required": False}}


class FollowTagListSerializer(serializers.ListSerializer):
    @staticmethod
    def get_related(instance):
        obj = FollowTag.objects.filter(user_id=instance.pk)
        return obj

    def update(self, instance, validated_data):
        obj = self.get_related(instance)
        for i in validated_data:
            for key in i:
                obj.create(tag_id=i[key].pk, user_id=instance.pk)
        return obj


class FollowTagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = FollowTag
        fields = ["tag_id", "tag"]
        list_serializer_class = FollowTagListSerializer
