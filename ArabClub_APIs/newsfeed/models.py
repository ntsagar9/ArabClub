from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User
from django.utils.text import slugify

STATUS_CHOICES = (
    ("draft", "Draft"),
    ("published", "Published"),
)


class Post(models.Model):
    """
    Note For Me
    Fix create_date field, update_date
    """

    title = models.CharField(max_length=150, verbose_name="Title")
    content = models.TextField(verbose_name="content")
    published_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now=timezone.now)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="published")
    slug = models.SlugField(null=False)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-published_at",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "newsfeed:post_details", kwargs={"slug": f"{self.slug}-{self.pk}"}
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Tag(models.Model):
    # TODO kill repeat tags in data base
    tag_name = models.CharField(max_length=50, verbose_name="Tag Name", unique=True)
    post = models.ForeignKey(Post, related_name="post_tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name

    def save(self, *args, **kwargs):
        tag = Tag.objects.filter(tag_name=self.tag_name)
        if tag.exists():
            tag = tag.first()
            print("exist", tag.pk)
            return tag
        return super(Tag, self).save(*args, **kwargs)


class FollowTags(models.Model):
    tags = models.ForeignKey(Tag, related_name="tag_fk", on_delete=models.CASCADE)

    user = models.ForeignKey(User, related_name="follow_tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.tags.tag_name

    def save(self, *args, **kwargs):
        tag = FollowTags.objects.filter(
            tags__tag_name=self.tags.tag_name, user_id=self.user.pk
        )
        if tag.exists():
            return tag.first()

        super(FollowTags, self).save(*args, **kwargs)


class Comments(models.Model):
    comment = models.TextField(verbose_name="Comment")
    create_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now_add=timezone.now)
    user = models.ForeignKey(
        User, related_name="user_comment_fk", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comment_fk", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment


class Reply(models.Model):
    reply = models.TextField(verbose_name="Reply comment")
    create_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now_add=timezone.now)
    user = models.ForeignKey(
        User, related_name="user_reply_fk", on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comments, related_name="reply_comment_fk", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.reply
