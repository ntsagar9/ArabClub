from django.db import models
from django.utils import timezone

from users.models import User


class Post(models.Model):
    """
    Note For Me
    Fix create_date field, update_date
    """
    title = models.CharField(max_length=150, verbose_name="Title")
    content = models.TextField(verbose_name='content')
    create_data = models.DateTimeField(auto_now_add=timezone.now)
    update = models.DateTimeField()
    user = models.ForeignKey(User, related_name='post',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, verbose_name='Tag Name')
    post = models.ForeignKey(Post,related_name='post_tags',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name
