from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", args=[self.pk])

    class Meta:
        ordering = ("-post_date",)


class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name="ألاسم")
    body = models.TextField(verbose_name="ألتعليق")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"علق : {self.name} علي : {self.post}"

    class Meta:
        ordering = ("-comment_date",)
