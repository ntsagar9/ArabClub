from django.db import models
from django.utils import timezone
from django.urls import reverse
from newsfeed.models import Post
from users.models import User


class Comment(models.Model):
    comment = models.TextField(verbose_name="Comment")
    create_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now=timezone.now)
    user = models.ForeignKey(
        User, related_name="user_comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('newsfeed:comment_sys:create_comment',
                       args=[self.post.slug, self.post.pk])



class Reply(models.Model):
    reply = models.TextField(verbose_name="Reply comment")
    create_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now_add=timezone.now)
    user = models.ForeignKey(
        User, related_name="user_replys", on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment, related_name="replys_comment", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.reply
