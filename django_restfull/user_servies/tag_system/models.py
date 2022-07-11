from django.db import models

# from newsfeed.models import Post
from user.models import User


class Tag(models.Model):
    tag = models.CharField(max_length=50, verbose_name="Tag Name", unique=True)
    # post = models.ForeignKey(
    #     Post, related_name="post_tags", on_delete=models.CASCADE
    # )

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        tag = Tag.objects.filter(tag=self.tag)
        if tag.exists():
            tag = tag.first()
            return tag
        return super().save(*args, **kwargs)


class FollowTag(models.Model):
    tag = models.ForeignKey(
        Tag, related_name="tag_fk", on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User, related_name="follow_tag", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.tag.tag

    def save(self, *args, **kwargs):
        # self.objects.get(tag__tag=)
        try:
            FollowTag.objects.get(tag__tag=self.tag.tag, user_id=self.user_id)
        except FollowTag.DoesNotExist:
            return super().save(*args, **kwargs)
